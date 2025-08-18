from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from google.cloud import vision
from PIL import Image
import io

app = FastAPI()
client = vision.ImageAnnotatorClient()

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Verify image with Pillow
        try:
            img = Image.open(io.BytesIO(contents))
            img.verify()
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Invalid image: {str(e)}"})

        # Call Vision API
        response = client.annotate_image({
            "image": {"content": contents},
            "features": [{"type_": vision.Feature.Type.LABEL_DETECTION}],
        })

        labels = [label.description for label in response.label_annotations]
        return {"labels": labels}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
