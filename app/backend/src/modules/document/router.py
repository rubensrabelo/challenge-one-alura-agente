from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.modules.document.service import DocumentService

router = APIRouter(prefix="/document", tags=["Documentos"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.csv')):
        raise HTTPException(status_code=400, detail="Apenas arquivos .pdf ou .csv são suportados.")
    try:
        message = await DocumentService.process_and_index(file)
        return {"status": "success", "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
