# Gerekli kütüphanelerin içe aktarılması
import json  # JSON işlemleri için
from fastapi import FastAPI, File, UploadFile  # FastAPI ve dosya yükleme ile ilgili sınıflar
from fastapi.responses import JSONResponse  # JSON formatında HTTP yanıtı vermek için
from transformers import pipeline  # (Kullanılmıyor ama muhtemelen ilerde AI ile işlenecek)
from PIL import Image  # Görsel işleme için Pillow (PIL) kütüphanesi
import pytesseract  # OCR (Optik Karakter Tanıma) işlemleri için Tesseract kütüphanesi

# FastAPI uygulaması oluşturuluyor
app = FastAPI()

# Ana (root) endpoint, API çalışıyor mu kontrolü için basit bir yanıt döner
@app.get("/")
def root():
    return {"message": "Hello from OCR-API!"}

# /extract endpoint'i, POST metoduyla çalışan bir OCR API'idir
# Kullanıcıdan bir görsel dosyası alır ve metni çıkarır
@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        # Yüklenen görseli aç, RGB formatına çevir
        image = Image.open(file.file).convert("RGB")
        
        # Türkçe dil desteğiyle OCR işlemi yap (görseldeki metni çıkar)
        extracted_text = pytesseract.image_to_string(image, lang="tur")

        # Çıkarılan metni JSON formatında döndür
        return JSONResponse(content={
            "raw_text": extracted_text,
        })

    except Exception as e:
        # Hata durumunda kullanıcıya hata mesajı döndür
        return JSONResponse(content={"error": str(e)}, status_code=500)
