import os
from typing import List

import torch
from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pdf2image import convert_from_path
from PIL import Image
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoProcessor

from colpali_engine.models.paligemma_colbert_architecture import ColPali
from colpali_engine.trainer.retrieval_evaluator import CustomEvaluator
from colpali_engine.utils.colpali_processing_utils import (
    process_images,
    process_queries,
)

app = FastAPI()
security = HTTPBearer()
BEARER_TOKEN = "NoDayShallEraseYouFromTheMemoryOfTime"


# read-only HF token with gemma access
token = "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"

# Load model
model_name = "vidore/colpali"
model = ColPali.from_pretrained(
    "google/paligemma-3b-mix-448",
    torch_dtype=torch.bfloat16,
    device_map="cuda",
    token=token,
).eval()
model.load_adapter(model_name)
processor = AutoProcessor.from_pretrained(model_name, token=token)
device = model.device
mock_image = Image.new("RGB", (448, 448), (255, 255, 255))

# Global variables to store indexed data
indexed_embeddings = []
indexed_images = []


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials


@app.get("/index/")
async def index_document(
    force_reindex: bool = False,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token),
):
    global indexed_embeddings, indexed_images

    print("Starting indexing process...")

    if indexed_embeddings and not force_reindex:
        print("Document already indexed. Skipping re-indexing.")
        return {
            "message": "Document already indexed. Use force_reindex=true to re-index."
        }

    file_path = "full_dgcl_2023_2024.pdf"
    if not os.path.exists(file_path):
        print(f"Error: PDF file not found at {file_path}")
        raise HTTPException(status_code=404, detail="PDF file not found")

    print("Converting PDF to images...")
    images = convert_from_path(file_path)
    indexed_images = images
    print(f"Converted {len(images)} pages to images.")

    print("Creating DataLoader...")
    dataloader = DataLoader(
        images,
        batch_size=4,
        shuffle=False,
        collate_fn=lambda x: process_images(processor, x),
    )

    print("Starting embedding generation...")
    indexed_embeddings = []
    for i, batch_doc in enumerate(tqdm(dataloader)):
        print(f"Processing batch {i+1}/{len(dataloader)}")
        with torch.no_grad():
            batch_doc = {k: v.to(device) for k, v in batch_doc.items()}
            embeddings_doc = model(**batch_doc)
        indexed_embeddings.extend(list(torch.unbind(embeddings_doc.to("cpu"))))

    print(f"Indexing complete. Total pages indexed: {len(images)}")
    return {"message": f"Indexed {len(images)} pages successfully"}


@app.get("/query/")
async def query_document(
    query: str = Query(..., description="The search query"),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token),
):
    global indexed_embeddings, indexed_images

    if not indexed_embeddings:
        raise HTTPException(
            status_code=400,
            detail="Document not indexed. Please index the document first.",
        )

    with torch.no_grad():
        batch_query = process_queries(processor, [query], mock_image)
        batch_query = {k: v.to(device) for k, v in batch_query.items()}
        embeddings_query = model(**batch_query)
        qs = list(torch.unbind(embeddings_query.to("cpu")))

    retriever_evaluator = CustomEvaluator(is_multi_vector=True)
    scores = retriever_evaluator.evaluate(qs, indexed_embeddings)

    # Get top 5 relevant pages
    top_pages = scores.argsort(axis=1)[0][-3:][::-1].tolist()

    return {"relevant_pages": [int(page) for page in top_pages]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
