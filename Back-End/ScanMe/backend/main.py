from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import pytesseract
import io
import os

app = FastAPI()

# Configurez le chemin de Tesseract si nécessaire
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Dossier pour sauvegarder temporairement les fichiers
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crée le dossier s'il n'existe pas


@app.get("/")
def read_root():
    """
    Endpoint racine pour vérifier que le serveur fonctionne.
    """
    return {"message": "Welcome to the ID Scanner API"}


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint pour téléverser une image et en extraire le texte avec OCR.
    """
    # Validation du type de fichier
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PNG or JPEG image.")

    try:
        # Sauvegarder temporairement le fichier
        file_location = f"{UPLOAD_FOLDER}/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Charger et prétraiter l'image
        image = Image.open(file_location)

        # Extraction du texte avec OCR
        text = pytesseract.image_to_string(image)

        # Supprimer le fichier temporaire après traitement
        os.remove(file_location)

        return {"filename": file.filename, "extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")
