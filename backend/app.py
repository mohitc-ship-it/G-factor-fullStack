from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from typing import List
from ragAnything import store_document
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from utils import append_to_json, load_reports, convert_json_format
from services import analyze_file, answer, anamolies_detection
import json
from excel_to_pdf import process_excel_for_rag

app = FastAPI()

# Enable CORS if frontend will call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    query: str

# Simple chat logic (replace with actual LLM integration)
def chat_with_user(message: str) -> str:
    return f"You said: {message}. This is a dummy response."

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response = await answer(req.query)
    return {"response": response}


# @app.post("/upload-reports")
# async def upload_report(files: List[UploadFile] = File(...)):

#     UPLOAD_ROOT = Path("uploaded_files")
#     UPLOAD_ROOT.mkdir(exist_ok=True)


#     session_id = str(uuid.uuid4())
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     session_dir = UPLOAD_ROOT / f"{timestamp}_{session_id}"
#     session_dir.mkdir(parents=True, exist_ok=True)


#     saved_files = []

#     reports = []
#     for file in files:
#         print("filename ",file.filename)
#         if "Plating" in file.filename :
#             print(":checking succ")
#             continue
#         unique_name = f"{uuid.uuid4()}_{file.filename}"
#         file_path = session_dir / unique_name


#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)


#         saved_files.append({
#         "original_name": file.filename,
#         "saved_name": unique_name,
#         "path": str(file_path)
#         })
#         excel_converted_paths = process_excel_for_rag(file_path)
#         if excel_converted_paths[0]!="normal flow":
#             files.extend(excel_converted_paths)
        
        

#         extracted_content_folder = await store_document(file_path)

#         report_obj =  {
#       "file_name": "TM-192_Plating_Bath_Analysis_Nickel_Baths.docx",
#       "file_type": "docx",
#       "file_path": "/data/context/TM-192_Plating_Bath_Analysis_Nickel_Baths.docx",
#       "extracted_content_folder": "/data/context/TM-192_Plating_Bath_Analysis_Nickel_Baths/",
#       "uploaded_on":"",
#       "file_summary": "Internal titration method for Nickel Sulfamate plating baths, with calculation formulas for Ni concentration and acidity.",
#       "anomalies_detected": [],
#       "rules_detected":[]
#     }
        
#         report_obj["extracted_content_folder"] = str(extracted_content_folder)
#         report_obj["file_name"] = unique_name
#         report_obj["file_path"] = str(file_path)
#         report_obj["uploaded_on"] = datetime.now().isoformat()
#         report_obj["file_type"] = file.filename.split(".")[-1]

#         report_obj = analyze_file(report_obj)
#         reports.append(report_obj)

#         # report_obj['file_data'] = file_analysis['summary']
#         # report_obj['anomalies_detected'] = file_analysis['anomalies']
#         # report_obj['rules'] = file_analysis['rules_detected']
    
#     for report_obj in reports:
#         report_obj = anamolies_detection(report_obj)
#         append_to_json("reports.json",report_obj)
    
#     report_json = load_reports()
#     final_report_json = convert_json_format(report_json)
#     print(final_report_json)
#     return final_report_json

@app.post("/upload-reports")
async def upload_report(files: List[UploadFile] = File(...)):
    # UPLOAD_ROOT = Path("uploaded_files")
    # UPLOAD_ROOT.mkdir(exist_ok=True)

    # session_id = str(uuid.uuid4())
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # session_dir = UPLOAD_ROOT / f"{timestamp}_{session_id}"
    # session_dir.mkdir(parents=True, exist_ok=True)

    # reports = []
    converted_paths = []

    # for file in files:
    #     print("filename", file.filename)

    #     if "Plating" in file.filename:
    #         print(":checking succ")
    #         continue

    #     unique_name = f"{uuid.uuid4()}_{file.filename}"
    #     file_path = session_dir / unique_name

    #     with open(file_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)

    #     # ✅ Excel detection + processing
    #     excel_converted_paths = process_excel_for_rag(file_path, out_dir=session_dir)
    #     if excel_converted_paths[0] != "normal flow" and excel_converted_paths[0] != "only_excel_inputs":
    #         converted_paths.extend(excel_converted_paths)

    #     # ✅ Proceed with normal doc extraction
    #     extracted_content_folder = await store_document(file_path)

    #     report_obj = {
    #         "file_name": unique_name,
    #         "file_type": file.filename.split(".")[-1],
    #         "file_path": str(file_path),
    #         "extracted_content_folder": str(extracted_content_folder),
    #         "uploaded_on": datetime.now().isoformat(),
    #         "file_summary": "",
    #         "anomalies_detected": [],
    #         "rules_detected": []
    #     }

    #     report_obj = analyze_file(report_obj)
    #     reports.append(report_obj)

    # # ✅ Anomaly detection + persistence
    # for report_obj in reports:
    #     report_obj = anamolies_detection(report_obj)
    #     append_to_json("reports.json", report_obj)

    report_json = load_reports()
    final_report_json = convert_json_format(report_json)

    print(final_report_json)
    # return {"reports": final_report_json, "converted_files": converted_paths}
    return final_report_json



    # return {"session_id": session_id, "saved_dir": str(session_dir), "files": saved_files}