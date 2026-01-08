import json
from pathlib import Path
from typing import Union, List, Dict
from dataclasses import asdict, is_dataclass
from datetime import datetime


def load_rules():
    with open("rules.json","r",encoding="utf-8") as f:
        rules = json.load(f)
    
    return rules


def load_reports():
    with open("reports.json","r",encoding="utf-8") as f:
        reports = json.load(f)
    
    return reports


def load_manufacturDetails():
    with open("manufacturerDetails.json","r",encoding="utf-8") as f:
        manuDetails = json.load(f)
    
    return manuDetails


# def append_to_json(file_path: str, obj: Union[Dict, List[Dict]]):
#     path = Path(file_path)

#     # Normalize input into a list of objects
#     if isinstance(obj, list):
#         new_items = obj
#     else:
#         new_items = [obj]

#     # If file doesn't exist → create new array
#     if not path.exists():
#         with open(path, "w") as f:
#             json.dump(new_items, f, indent=4)
#         return

#     # Try reading existing JSON data
#     try:
#         with open(path, "r") as f:
#             data = json.load(f)

#         # Normalize existing data to list
#         if not isinstance(data, list):
#             data = [data]

#     except Exception:
#         # If corrupted, start fresh
#         data = []

#     # Append new items
#     data.extend(new_items)

#     # Save back to file
#     with open(path, "w") as f:
#         json.dump(data, f, indent=4)


# def append_to_json(file_path: str, obj: Union[Dict, List[Dict]]):
#     path = Path(file_path)

#     def to_serializable(o):
#         """Convert Pydantic models, dataclasses, or other custom objects to dicts."""
#         # Pydantic v2 models
#         if hasattr(o, "model_dump") and callable(o.model_dump):
#             return o.model_dump()
#         # Pydantic v1 models
#         if hasattr(o, "dict") and callable(o.dict):
#             return o.dict()
#         # Dataclasses
#         if is_dataclass(o):
#             return asdict(o)
#         # Other objects with __dict__
#         if hasattr(o, "__dict__"):
#             return o.__dict__
#         # Fallback to string
#         return str(o)

#     # Normalize input into a list of objects
#     new_items = obj if isinstance(obj, list) else [obj]
#     new_items = [to_serializable(i) for i in new_items]

#     # If file doesn't exist → create new array
#     if not path.exists():
#         with open(path, "w") as f:
#             json.dump(new_items, f, indent=4, default=to_serializable)
#         return

#     # Try reading existing JSON data
#     try:
#         with open(path, "r") as f:
#             data = json.load(f)
#         if not isinstance(data, list):
#             data = [data]
#     except Exception:
#         data = []

#     # Append and save back
#     data.extend(new_items)
#     with open(path, "w") as f:
#         json.dump(data, f, indent=4, default=to_serializable)

def append_to_json(file_path: str, obj: Union[Dict, List[Dict], str]):
    path = Path(file_path)

    def to_serializable(o):
        """Recursively convert custom objects into plain JSON-serializable types."""
        # If it's already a dict/list/str/int/float/bool/None — safe
        if isinstance(o, (dict, list, str, int, float, bool)) or o is None:
            return o

        # If it's a JSON string (try parsing it)
        if isinstance(o, str):
            try:
                return json.loads(o)
            except Exception:
                return o  # keep as string if not valid JSON

        # Pydantic v2
        if hasattr(o, "model_dump") and callable(o.model_dump):
            return to_serializable(o.model_dump())

        # Pydantic v1
        if hasattr(o, "dict") and callable(o.dict):
            return to_serializable(o.dict())

        # Dataclass
        if is_dataclass(o):
            return to_serializable(asdict(o))

        # Custom class
        if hasattr(o, "__dict__"):
            return to_serializable(o.__dict__)

        # Fallback only for unsupported primitive
        return str(o)

    # --- Normalize obj into list and parse if it's a JSON string
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except Exception:
            pass

    new_items = obj if isinstance(obj, list) else [obj]
    new_items = [to_serializable(i) for i in new_items]

    # --- Load existing data (or create new)
    if path.exists():
        try:
            with open(path, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = [data]
        except Exception:
            data = []
    else:
        data = []

    # --- Merge and save
    data.extend(new_items)
    with open(path, "w") as f:
        json.dump(data, f, indent=4, default=to_serializable)


def read_md(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Markdown file not found: {file_path}")

    return path.read_text(encoding="utf-8")


def get_single_md_file(folder_path: str) -> Path | None:
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise NotADirectoryError(f"Not a valid folder: {folder_path}")

    # recursively search all subdirectories for .md files
    md_files = list(folder.rglob("*.md"))

    if len(md_files) == 0:
        return None  # no markdown file found anywhere

    if len(md_files) > 1:
        raise ValueError(f"More than one .md file found in {folder_path} (found {len(md_files)})")

    return md_files[0]  # the only md file found




def convert_json_format(initial_json):
    """
    Convert initial JSON (list of file entries) into the new target JSON format.
    """

    final_json = []

    for file_entry in initial_json:
        new_entry = {
            "file_name": file_entry.get("file_name"),
            "file_type": file_entry.get("file_type"),
            "file_path": file_entry.get("file_path"),
            "extracted_content_folder": file_entry.get("extracted_content_folder"),
            "uploaded_on": datetime.utcnow().isoformat(),
            "file_summary": file_entry.get("file_summary", ""),
        }

        # --- anomalies_detected mapping ---
        anomalies = file_entry.get("anomalies_detected", {}).get("anomalies_detected", [])
        new_entry["anomalies_detected"] = [
            {
                "anomaly_desc": a.get("anomaly_desc"),
                "anomaly_rule_detail": a.get("anomaly_rule_detail"),
                "anomaly_rule_source_file": a.get("anomaly_rule_source_file"),
                "suggested_solution": a.get("suggested_solution"),
            }
            for a in anomalies
        ]

        # --- rules_detected mapping ---
        rules = file_entry.get("rules_detected", [])
        new_entry["rules_detected"] = [
            {
                "rule_desc": r.get("rule_name"),
                "rule_source_file": (
                    file_entry.get("file_name")
                    if file_entry.get("file_name")
                    else None
                ),
                "rule_detail": r.get("rule_definition"),
            }
            for r in rules
        ]

        final_json.append(new_entry)

    return final_json

