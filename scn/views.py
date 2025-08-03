from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import SCNUpload
from .serializers import SCNUploadSerializer
from django.conf import settings
from .utils import extract_text_auto
import os
import fitz  # PyMuPDF  
from search_weaviate import answer_query
from .utils import chunk_text, get_embeddings
from .weaviate_client import upload_chunks

# Create your views here.
class SCNUploadView(APIView):
    """API endpoint for uploading SCN (PDF) files, extracting text, chunking, embedding, and uploading to Weaviate."""
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        """Handle file upload, text extraction, chunking, embedding, and upload to Weaviate."""
        serializer = SCNUploadSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            file_path = os.path.join(settings.MEDIA_ROOT, str(instance.file))

            try:
                extracted_text = extract_text_auto(file_path)
                print(f"extracted_text: {extracted_text}")
                instance.extracted_text = extracted_text
                instance.save()

                # --- Chunking and Embedding ---
                chunks = chunk_text(extracted_text)
                embeddings = get_embeddings(chunks)
                upload_chunks(chunks, embeddings, source=str(instance.file))

                return Response({
                    'file': serializer.data['file'],
                    'extracted_text': extracted_text
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    'error': f"File saved but failed to extract text: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AskQuestionAPI(APIView):
    """API endpoint for answering user questions using vector search and LLM over uploaded content."""
    def post(self, request):
        """Handle user query, search for relevant chunks, and generate an answer using LLM."""
        query = request.data.get("query")
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        answer = answer_query(query)
        return Response({
            "query": query,
            "answer": answer
        }, status=status.HTTP_200_OK)
