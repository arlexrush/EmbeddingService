import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import asyncio

app = FastAPI()

# Modelo para validar la entrada de datos en el cuerpo
class TextInput(BaseModel):
    text: str

# Carga el modelo de forma asíncrona
async def load_model():
    return SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

model = None

@app.on_event("startup")
async def startup_event():
    global model
    model = await load_model()

@app.post("/embed")
async def generate_embedding(input_Data: TextInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        embedding = await asyncio.to_thread(model.encode, input_Data.text)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Usar el puerto de la variable de entorno PORT
    print(f"Server will run on port: {port}")  # Imprime el valor de 'port'
    uvicorn.run(app, host="0.0.0.0", port=port)