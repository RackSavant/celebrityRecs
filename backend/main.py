import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
import torch
import uuid

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and processor
MODEL_NAME = "nateraw/vit-fashion-classifier"
extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
model.eval()

# Map model classes to eras (simple mapping for MVP)
CATEGORY_TO_ERA = {
    'Blazer': '1980s',
    'Blouse': '1940s',
    'Dress': '1960s',
    'Jeans': '1970s',
    'Jacket': '1990s',
    'Shorts': '1990s',
    'Skirt': '1950s',
    'Sweater': '1950s',
    'Tee': '1990s',
    'Top': '1940s',
    'Trousers': '1940s',
    'Cardigan': '1950s',
    'Tank': '1990s',
    'Romper': '1970s',
    'Jumpsuit': '1970s',
    'Hoodie': '1990s',
    'Pants': '1970s',
    'Coat': '1940s',
    'Sweatshirt': '1990s',
    'Vest': '1980s',
    'Polo': '1980s',
    'Turtleneck': '1960s',
    'Kimono': '1970s',
    'Poncho': '1970s',
    'Cape': '1940s',
    'Overalls': '1970s',
    'Suit': '1980s',
    'Shirt': '1940s',
    'Other': '1990s',
}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Save image
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())
    # Open and preprocess image
    image = Image.open(filepath).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0]
        conf, pred_idx = torch.max(probs, 0)
        conf = float(conf)
        pred_idx = int(pred_idx)
        pred_class = model.config.id2label[pred_idx]
    era = CATEGORY_TO_ERA.get(pred_class, '1990s')
    # Compose response
    return JSONResponse({
        "filename": filename,
        "image_url": f"/images/{filename}",
        "predicted_class": pred_class,
        "era": era,
        "confidence": round(conf * 100, 2)
    })

@app.get("/images/{filename}")
def get_image(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return JSONResponse({"error": "Not found"}, status_code=404)
    return FileResponse(filepath) 