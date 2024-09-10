from fastapi import FastAPI, Body
from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio
import concurrent.futures



# Crear el ThreadPoolExecutor a nivel global
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# Inicializar la app FastAPI
app = FastAPI()

# Load the pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor()

@app.post("/generate-embeddings")
async def generate_embeddings(text: str = Body(..., embed=True)):
    # Define a function to generate the embeddings
    def generate_embeddings_sync(text):
        #embeddings = await asyncio.to_thread(model.encode, text, convert_to_numpy=True)
        embeddings = model.encode(text, convert_to_numpy=True)
        return embeddings.tolist()

   # Generate the embeddings asynchronously
    loop = asyncio.get_running_loop()
    embeddings = await loop.run_in_executor(executor, generate_embeddings_sync, text)

    return {"embeddings": embeddings}