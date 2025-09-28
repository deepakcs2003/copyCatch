from fastapi import FastAPI, HTTPException, Query
from app.preProcessing import save_to_db, extract_and_preprocess
from app.db import documents_col
from app.Model.preProcessingModel import UploadRequest
from app.hashFunction import make_hash_funcs

app = FastAPI()

@app.get("/")
def read_root():

    return {"message": "Hello, COPYCATCH! MongoDB is connected."}

@app.get("/hash-funcs/")
def get_hash_funcs():
    funcs = make_hash_funcs()
    return {"num_funcs": funcs}

@app.post("/upload/")
def upload_file(request: UploadRequest):
    try:
        # Access fields from request
        file_url = request.file_url
        submission_id = request.submission_id
        assignment_id = request.assignment_id

        inserted_id = save_to_db(file_url, submission_id,assignment_id)

        return {
            "message": "File processed and saved to DB",
            "id": inserted_id,
            "submission_id": submission_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{doc_id}")
def get_document(doc_id: str):
    if not documents_col:
        raise HTTPException(status_code=500, detail="Database not connected")
    doc = documents_col.find_one({"_id": doc_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": str(doc["_id"]), "raw_text": doc["raw_text"], "processed_text": doc["processed_text"]}
