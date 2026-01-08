import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from utils import load_manufacturDetails


load_dotenv()

# ---------- Normal text output ----------
def llm_query(query: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    # llm = llm.bind(tools=[{"type": "web_search"}])
    message = HumanMessage(content=f"Answer this question:\n{query}")
    return llm.invoke([message]).content


def llm_with_search(query:str):
    client = OpenAI()

    manuDetails = load_manufacturDetails()

    prompt = f"""answer the query in concise manner keeping only important information Query: """+query 
    if len(manuDetails) > 0:
        prompt = prompt +  f""" /n currently we have some details about product and there manufacturers might help if nay product in question matches , then search specifci website to that product from below, else search as per question directly"
    Manufacturer details:
    {manuDetails}"""

    response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    tools=[{"type": "web_search"}],
)
    return response.output_text

# ---------- Structured output with schema ----------
def llm_structured(query: str, output_schema: BaseModel):
    print("query is ", query)
    """
    query: str -> user question
    output_schema: pydantic BaseModel -> defines structured output
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    # Bind the schema to the LLM
    llm_with_structure = llm.with_structured_output(output_schema)
    
    # Invoke the LLM
    return llm_with_structure.invoke(query)


print("solution is ")
# print(llm_with_search("get me a troubleshooting example from agilant"))
# print(llm_with_search("latest pune news"))