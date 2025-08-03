import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError

from dotenv import load_dotenv

load_dotenv()

# Load environment variables directly
WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY = os.environ["WEAVIATE_API_KEY"]
HF_API_KEY = os.environ["HF_API_KEY"]  # Assuming SentenceTransformer embeddings

# Initialize Weaviate client
try:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        headers={"X-HuggingFace-Api-Key": HF_API_KEY},
    )
except WeaviateBaseError as e:
    raise RuntimeError(f"[❌] Failed to connect to Weaviate Cloud: {str(e)}")

def test_connection():
    """Test if the Weaviate client is ready and connected."""
    if client.is_ready():
        print("[✅] Connected to Weaviate Cloud successfully.")
    else:
        raise Exception("[❌] Weaviate client is not ready.")

def create_weaviate_schema():
    """Create the 'LegalChunk' collection in Weaviate if it does not exist."""
    class_name = "LegalChunk"
    existing_collections = client.collections.list_all()
    
    if class_name not in existing_collections:
        client.collections.create(
            name=class_name,
            properties=[
                {"name": "text", "data_type": "text"},
                {"name": "source", "data_type": "text"}
            ],
            vector_config={"vectorizer": "none"}
        )
        print("[📦] Weaviate schema 'LegalChunk' created.")
    else:
        print("[ℹ️] Schema 'LegalChunk' already exists.")

def upload_chunks(chunks, embeddings, source):
    """Upload text chunks and their embeddings to the 'LegalChunk' collection in Weaviate."""
    class_name = "LegalChunk"
    collection = client.collections.get(class_name)

    print(f"[⬆️] Uploading {len(chunks)} chunks to Weaviate...")

    for chunk, vector in zip(chunks, embeddings):
        collection.data.insert(
            properties={
                "text": chunk,
                "source": source
            },
            vector=vector
        )

    print("[✅] Upload complete.")
