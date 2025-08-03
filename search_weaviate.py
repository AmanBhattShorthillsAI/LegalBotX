from sentence_transformers import SentenceTransformer
import weaviate
import os
from weaviate.classes.query import Filter, MetadataQuery
from weaviate.classes.init import Auth
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY = os.environ["WEAVIATE_API_KEY"]
HF_API_KEY = os.environ["HF_API_KEY"]

# Init client
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={"X-HuggingFace-Api-Key": HF_API_KEY},
)

# Load same embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_legal_chunks(query, top_k=3):
    # Convert query to embedding
    query_embedding = model.encode(query).tolist()

    # Access collection
    collection = client.collections.get("LegalChunk")

    # Perform vector search
    results = collection.query.near_vector(
        near_vector=query_embedding,
        limit=top_k,
        return_metadata=MetadataQuery(distance=True),
    )

    # Extract and return relevant chunks
    relevant_chunks = [
        {
            "text": o.properties["text"],
            "source": o.properties.get("source", ""),
            "distance": o.metadata.distance,
        }
        for o in results.objects
    ]

    return relevant_chunks

from langchain_openai import AzureChatOpenAI

openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    temperature=0.0,
    max_tokens=1000,
    openai_api_key=openai_api_key,
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)

def generate_answer_from_context(query, context):
    prompt = f"""You are a helpful and knowledgeable assistant. Use the provided context to answer the user's question as accurately and clearly as possible.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer in a clear, concise, and helpful manner."""

    response = llm.invoke(prompt, temperature=0.0, max_tokens=1000)
    return response.content

def answer_query(query):
    chunks = search_legal_chunks(query, top_k=3)
    if not chunks:
        return "Sorry, I couldn't find relevant information."

    # Combine the text from the top 3 chunks
    context = "\n\n".join(chunk["text"] for chunk in chunks)
    return generate_answer_from_context(query, context)

