from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import numpy as np
import asyncio
import concurrent.futures



# Crear el ThreadPoolExecutor a nivel global
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# Inicializar la app FastAPI
app = FastAPI()

# Load the pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

tokenizer = AutoTokenizer.from_pretrained('paraphrase-multilingual-mpnet-base-v2')
tokens = tokenizer.tokenize("Tu texto aquí", clean_up_tokenization_spaces=False)

# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor()

@app.post("/generate-embeddings")
async def generate_embeddings(text: str = Body(..., embed=True)):
    # Define a function to generate the embeddings
    async def generate_embeddings_sync(text):
        try:
            embeddings = await asyncio.to_thread(model.encode, text, convert_to_numpy=True)
            #embeddings = model.encode(text, convert_to_numpy=True)
            return {"embeddings": embeddings.tolist()} 
                    #embeddings.tolist()
        except Exception as e:
            return {"error": f"Error generating embeddings: {str(e)}"}
        
   # Generate the embeddings asynchronously
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, generate_embeddings_sync, text)
    #embeddings = await loop.run_in_executor(executor, generate_embeddings_sync, text)

    return  result
            #{"embeddings": embeddings}
            
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})