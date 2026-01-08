from ragAnything import query_rag
from llm import llm_query, llm_structured, llm_with_search
from utils import load_rules,read_md,get_single_md_file, append_to_json, load_reports
from pydantic import BaseModel
from typing import List, Optional


# MODELS
class RuleParameters(BaseModel):
    type: str
    fields: Optional[List[str]] = None


class DetectedRule(BaseModel):
    rule_name: str
    rule_definition: str
    applies_on: List[str]
    parameters: RuleParameters
    severity: str
    action_on_violation: str
    extracted_from: Optional[List[str]] = None

class ManufacturerDetails(BaseModel):
    manufacturer_name:str
    product_name:str

class RuleExtractionOutput(BaseModel):
    file_summary: str
    detected_rules: List[DetectedRule]
    manufacturer_details_list: List[ManufacturerDetails]



class AnomalyItem(BaseModel):
    anomaly_desc: str
    anomaly_rule_detail: str
    anomaly_rule_source_file: str
    suggested_solution: str


class AnomalyDetectionOutput(BaseModel):
    anomalies_detected: List[AnomalyItem]


# FUNCTIONS

async def answer(question):
    reports_data = load_reports()
    print("rports ", reports_data)
    ask_prompt12 = f""""check if user question is related and answerable correctly or answer is value of key from the reports json:  {reports_data} if yes then give answer with hierarchial formatting and spacing,
    else return "no" as 1 word answer,also its possible that it is related to trobleshotting and asking for web search then return word 'troubleshooting'
    user question is : {question}"""
    ask_prompt = f"""Task:
Analyze the user's question and determine whether it can be answered using the provided reports_data JSON.

Instructions:
if question is about logsheet and answer is available in below context logs data then provide answer.

If the question directly relates to information available in reports_data (e.g., keys, values, or logically inferable details), respond only with the correct answer derived from it.

If the question appears to be about troubleshooting, diagnostics, or requires external web information, respond only with the single word "troubleshooting".

If the question is unrelated to reports_data and not troubleshooting-related, respond only with the single word "no".

Input:

reports_data: {reports_data}

user_question: {question}

Output:

Either:

a direct answer from reports_data , correctly formatted (not in json), or

the word "no", or

the word "troubleshooting"""
    


#     ask_prompt  = ask_prompt + """ \nrefer some context about logsheet/logs data/log table below\n.  										Titration results			
# Date	Part name/task explanation	Temperature, C	Current, Amp	Time, min	Coating thickness, um	Total Bath Ampxhour after plating part in line	pH Preplate	Surface Tension	Pickle %HCL	Nickel Sulfamate Tetrahydrate, g/L	Boric acid, g/L	Nickel Cloride Hexahydrate, g/L	Notes
# 15-Nov	chemical add	70	9			274.5							added 11.5 L of Liquid Nickel Sulfate
# 15-Nov	125407 roll	70	9	80	35	286.5	4		30	575	19	14	
# 18-Nov	Start of day sample	70				286.5	4.1		30	570	17	14	filter cleaned and all filter pads changed to carbon filter pads
# 18-Nov	125408 roll	70	9	80	35	298.5	4						
# 18-Nov	125409 roll	70	9	80	35	310.5	4.2						
# 19-Nov	Start of day analysis					310.5		48.8	28	575	17	13	Surface tension was high, it should be less than 45. Sodium lauryl sulfate (SLS) needs to be added
# 19-Nov	Chemical add												Added 60 ml of wetter
# 19-Nov	125410 roll	70	9	80	35	322.5	4.5						
# 19-Nov	125411 roll	70	9	80	35	334.5	4						
# 19-Nov	125412 roll	70	9	80	35	346.5	4						
# 20-Nov	Start of day analytical							44.0	25%	575	17	13	%HCl in pickle was low. It should be around 30%. HCl needs to be added to pickle.
# 20-Nov	Chemical add												3 gallons HCl was added to pickle
# 20-Nov	125413 roll	70	9	80	35	358.5	4						
# 20-Nov	125414 roll	70	9	80	35	370.5	4						
# 20-Nov	125415 roll	70	9	80	35	382.5	4						
# 20-Nov	125416 roll	70	9	80	35	394.5	4						Cracked deposit. Based on the AA analysis, there is chrome contamination.


# Pickle tank				
# 	Composition			
# Time, min	Hydrocloric acid%			
# 5	30			
				
# Nickel Sulfamate tank				
# 	Composition			
# Temperature, C	Nickel Sulfamate Tetrahydrate, g/L	Boric acid, g/L	Nickel Cloride Hexahydrate, g/L	Sodium lauryl sulfate (SLS), g/L
# 60	580	18	15	0.37


# these are some log infromation too if required"""
    print("ask prompt ", ask_prompt)
    llm_answer =  llm_query(ask_prompt)

    print("llm answer is ", llm_answer)

    # if "troubleshooting" in llm_answer.split():
    #     response = llm_with_search(question)
    #     return response
    
    if "no" in llm_answer.split() or  "troubleshooting" in llm_answer.split():
        response = await query_rag(question)
        return response
    return llm_answer



def analyze_file(report_obj):
    extracted_content_folder = report_obj.get('extracted_content_folder', '')
    md_file_path = get_single_md_file(extracted_content_folder)
    file_data = read_md(md_file_path)

#     rules_detection_summary_prompt = f"""
# You are an expert data analyst and compliance AI specialized in understanding technical, chemical, and operational documents.

# You will be given the extracted content of a file.
# Your job is to analyze it carefully and return a **structured JSON** output with:
# 1. A concise **summary** of what the file contains (purpose, process, or data type).
# 2. Any **rules, procedures, or measurable limits** explicitly or implicitly mentioned in the text (e.g., "Acetylene pressure should not exceed 15 PSI", "pH range 4.0–5.0", etc.).
# 3. For each rule, include what it applies to and any threshold values if available.


# ### Guidelines:
# - Extract *only factual operational rules or limits* (ignore general instructions unless they define a measurable condition).
# - Keep numerical precision (e.g., 11 PSI, 15 PSI).
# - If no explicit numeric range, set type as "condition" and describe it clearly.
# - If rule boundaries are implicit, infer them logically but note it’s inferred.
# - Maintain neutral, technical tone.

# ---

# Now analyze the following file content:

# <file_content>
# {file_data}
# </file_content>
# """ 
    rules_detection_summary_prompt = f"""
You are an expert compliance analyst for technical, chemical, and operational documents.

You will be given extracted content from a file. Analyze it and return **structured JSON** with:
1) "summary": A concise 1–3 sentence summary of the file contents.
2) "rules_detected": Extract ONLY statements that are explicitly written as normative rules/specs/limits.

### RULE DETECTION — STRICT MODE

A statement qualifies as a RULE **only if the text explicitly contains** at least one of the following **normative or spec-triggering cues**:

#### 1. Normative modals/verbs (explicit only):
- "must", "shall", "should"
- "is required to", "needs to", "has to", "ought to", "is to"
- "ensure", "maintain", "keep"

#### 2. Constraint/spec words (explicit only):
- "limit", "maximum", "minimum"
- "upper limit", "lower limit"
- "range", "between", "within"
- "not exceed", "no more than", "at least", "not less than"

#### 3. Explicit specification/target words:
- "specification", "spec", "target", "setpoint", "nominal"
- "around", "approximately", "≈", "±"

#### 4. Explicit permissibility words:
- "allowed", "permissible", "acceptable"

#### 5. Tables that clearly mark a **rule** via explicit labels:
- Any table row or cell containing **Spec / Specification / Limit / Maximum / Minimum / Range / Target / Setpoint**.

If the text does not explicitly state a rule using the above cues, **do NOT treat it as a rule**.  
No inference. No interpretation. No guessing.

---

### EXCLUDE (never treat as rules):
- Pure measurements, logs, readings, time/value tables.
- Facts, descriptions, notes, background information.
- Instructions without measurable criteria.
- Any statement that does NOT contain a rule cue exactly as written.

---

### Mapping rules (only if cues are present):
- If text explicitly says “should be around 30%” → type: "target", approx: true.
- If text explicitly says “4.0–5.0 (spec)” → type: "range".
- If text explicitly uses “not exceed 8.5” → type: "max".
- If text explicitly uses “at least 60%” → type: "min".
- If text is qualitative but normative (“must be continuous”) → type: "condition".

No rule cue = no rule detected.

---

Return JSON ONLY.

<file_content>
{file_data}
</file_content>
"""


    rules_detection_summary_obj = llm_structured(rules_detection_summary_prompt,RuleExtractionOutput)

    print("rules ", rules_detection_summary_obj)
    
    report_obj["file_summary"] = rules_detection_summary_obj.file_summary
    report_obj['rules_detected'] = rules_detection_summary_obj.detected_rules
    append_to_json("rules.json",report_obj['rules_detected'])

    append_to_json("manufacturerDetails.json",rules_detection_summary_obj.manufacturer_details_list)
    return report_obj

def anamolies_detection(report_obj):
    extracted_content_folder = report_obj.get('extracted_content_folder', '')
    md_file_path = get_single_md_file(extracted_content_folder)
    file_data = read_md(md_file_path)

    rules = load_rules()
    anomlies_detection_prompt = f"""
You are an expert AI system responsible for detecting anomalies or out-of-spec conditions
in technical or chemical data by comparing it against defined operational rules.

You will receive:
1. The structured content extracted from a file (e.g., measurement data, logs, process values, etc.)
2. The list of all defined rules (from multiple documents)
3. Your goal is to:
   - Identify which rules are violated by the data
   - Describe the anomaly in detail (where, why, what)
   - Include which rule caused it and from which source file it came
   - Suggest a possible solution based on technical reasoning or safety practices

---

### INPUT DATA:
#### File Data:
{file_data}

#### Rules JSON:
{rules}


### INSTRUCTIONS:
- Be factual and technical; no generic or uncertain language.
- If multiple rules apply to the same parameter, list all violations.
- If no rule is violated, return an empty list under "anomalies_detected".
- Reference the rule source (from the JSON field `source_reference` or similar).
- Suggest solutions that are practical and based on domain knowledge (e.g., "adjust pH", "recalibrate instrument", "replace filter", etc.).

---

Now, using the above instructions, compare the provided file data against the rules and identify all anomalies.
"""

    report_obj['anomalies_detected'] = llm_structured(anomlies_detection_prompt,AnomalyDetectionOutput)

    return report_obj