# Backend testing report
import os
import requests

# API endpoint
API_URL = "http://localhost:8000/upload-reports"



def upload_files(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            files.append(("files", open(file_path, "rb")))
    
    if not files:
        print("⚠️ No files found in the folder.")
        return

    print(f"📤 Uploading {len(files)} files to {API_URL} ...")

    try:
        response = requests.post(API_URL, files=files)
        print("✅ Response status:", response.status_code)
        print("📄 Response body:", response.text)
    except Exception as e:
        print("❌ Upload failed:", e)
    finally:
        for _, f in files:
            f.close()

if __name__ == "__main__":
    upload_files("files")
