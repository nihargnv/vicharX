from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentForm
from .models import Document
import os
from django.conf import settings
from django.http import JsonResponse
from extract_file_content import extract_docx, extract_image, extract_pdf, extract_pptx, extract_excel, text_summarization, category
from django.views.decorators.csrf import csrf_exempt
import datetime
import mimetypes
import time

from django.db import connection
from django.utils.timezone import localtime
from django.db.models import Q
from django.db.models import Count

def analytics_view(request):
    total_documents = Document.objects.count()
    category_distribution = (
        Document.objects.values("category")
        .annotate(count=Count("category"))
        .order_by("-count")
    )

    return render(
        request,
        "analytics.html",
        {
            "total_documents": total_documents,
            "category_distribution": category_distribution,
        },
    )

def search_documents(request):
    """
    View for handling different types of document searches:
    - Keyword search: Searches in filenames, summary, and metadata
    - Date search: Filters documents by creation date
    - Semantic search: Simple implementation for natural language search
    """
    results = None
    search_type = request.GET.get('search_type', 'keyword')
    
    if search_type == 'keyword':
        keyword = request.GET.get('keyword', '')
        if keyword:
            # Search in filename, summary, and metadata
            results = Document.objects.filter(
                Q(file__icontains=keyword) | 
                Q(summary__icontains=keyword) | 
                Q(category__icontains=keyword)
            )
            
    elif search_type == 'date':
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            # Use metadata json field to filter by creation date
            # This assumes metadata has a 'creation_date' key
            results = Document.objects.filter(
                metadata__creation_date__gte=date_from.strftime('%Y-%m-%d')
            )
            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            if results:
                results = results.filter(
                    metadata__creation_date__lte=date_to.strftime('%Y-%m-%d')
                )
            else:
                results = Document.objects.filter(
                    metadata__creation_date__lte=date_to.strftime('%Y-%m-%d')
                )
                
    elif search_type == 'semantic':
        # Basic implementation of semantic search
        # In a real implementation, you would use embeddings or an NLP service
        query = request.GET.get('keyword', '')
        if query:
            # For now, do a more flexible keyword search as simplified semantic search
            keywords = query.lower().split()
            q_objects = Q()
            
            for keyword in keywords:
                q_objects |= Q(summary__icontains=keyword)
                q_objects |= Q(metadata__icontains=keyword)
                q_objects |= Q(category__icontains=keyword)
                
            results = Document.objects.filter(q_objects)
    
    context = {
        'results': results,
        'search_query': request.GET.get('keyword', ''),
        'search_type': search_type,
    }
    
    return render(request, 'search.html', context)

def document_view(request, document_id):
    """View for displaying a document's details"""
    try:
        document = Document.objects.get(id=document_id)
        return render(request, 'document_view.html', {'document': document})
    except Document.DoesNotExist:
        return render(request, 'search.html', {'error': 'Document not found'})

def document_download(request, document_id):
    """View for downloading a document"""
    from django.http import FileResponse, Http404
    import os
    
    try:
        document = Document.objects.get(id=document_id)
        file_path = document.file.path
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            raise Http404("File does not exist")
    except Document.DoesNotExist:
        raise Http404("Document does not exist")
    



def analytics(request):
    return render(request, "analytics.html")





def smart_search_view(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"error": "Search query is empty"}, status=400)

    # Step 1: Try finding an exact match in metadata["Name"] (if applicable)
    exact_match = Document.objects.filter(metadata__Name__icontains=query)

    if exact_match.exists():
        return JsonResponse({"results": list(exact_match.values("id", "metadata", "summary"))})

    # Step 2: Use Full-Text Search on the `summary` field via `document_fts`
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT doc_id FROM document_fts WHERE summary MATCH ? ORDER BY rank DESC", [query]
        )
        result_ids = [row[0] for row in cursor.fetchall()]

    # Fetch the matching Document objects
    results = Document.objects.filter(id__in=result_ids).values("id", "metadata", "summary")

    return JsonResponse({"results": list(results)})

def get_metadata(file_path):
    """Retrieve file metadata given a file path."""
    try:
        if not os.path.exists(file_path):
            return {"INFO": "File not found"}

        metadata = {}
        file_stat = os.stat(file_path)
        size_bytes = file_stat.st_size

        # Format file size in appropriate units
        if size_bytes < 1024:
            size_str = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes/1024:.1f} KB"
        else:
            size_str = f"{size_bytes/(1024*1024):.1f} MB"

        metadata["Name"] = os.path.basename(file_path)
        metadata["Size"] = size_str
        metadata["Created"] = time.ctime(file_stat.st_ctime)
        metadata["Modified"] = time.ctime(file_stat.st_mtime)
        metadata["Type"] = mimetypes.guess_type(file_path)[0] or "Unknown"

        return metadata
    except Exception as e:
        return {"INFO": f"Error retrieving metadata: {str(e)}"}

def classify_and_extract(file_path):
    file_type = str(file_path).split(".")[1]
    print("File Path: ", file_path)
    print("File Type: ", file_type)
    if file_type=='docx':
        summary = extract_docx.extract_text_from_docx(file_path)
    elif file_type.lower() == 'png' or file_type.lower() == 'jpg' or file_type.lower() == 'jpeg':
        summary = extract_image.process_image(file_path)
    elif file_type.lower() == 'pdf':
        summary = extract_pdf.extract_text_from_pdf(file_path)
    elif file_type.lower() == 'pptx':
        summary = extract_pptx.extract_text_from_pptx(file_path)
    elif file_type.lower() == 'xlsx':
        summary = extract_excel.extract_text_from_excel(file_path)
    else: 
        summary = "No Summary"

    summary = text_summarization.summarize(summary)
    cat = category.categorize_text(summary=summary)

    metadata = get_metadata(file_path)
    return cat, metadata, summary

def document_details(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    # Extract metadata if not already stored
    file_path = document.file.path
    file_size = os.path.getsize(file_path)  # File size in bytes
    file_type = os.path.splitext(file_path)[1]  # File extension

    

    # If metadata is not stored in the model, save it
    if not document.metadata:
        document.metadata = {}
        document.save()

    return render(
        request,
        "document_details.html",
        {"document": document, "metadata": document.metadata},
    )

def get_documents(request):
    documents = Document.objects.all()
    data = [
        {
            "id": doc.id,
            "name": doc.file.name,
            "category": doc.category, # Assuming tags are stored as comma-separated
            "preview": doc.file.url,  # Ensure this is a valid URL path
            "summary": doc.summary,
        }
        for doc in documents
    ]
    return JsonResponse({"documents": data})

@csrf_exempt  # Remove this if using CSRF token in the request
def delete_document(request, document_id):
    if request.method == "DELETE":
        document = get_object_or_404(Document, id=document_id)
        
        # Delete the file from storage
        if document.file:
            file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete the document record
        document.delete()
        
        return JsonResponse({"message": "Document deleted successfully."}, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def search(request):
    return render(request, "search.html")

def show_docs(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_path = os.path.join(settings.MEDIA_ROOT, "documents", uploaded_file.name)

            # Check if the file already exists
            existing_doc = Document.objects.filter(file=f"documents/{uploaded_file.name}").first()
            if existing_doc:
                message = "This file already exists!"
            else:
                category, metadata, summary = classify_and_extract(file_path)
                doc = Document(file=uploaded_file, category=category, summary=summary, metadata=metadata)
                doc.save()
                return redirect("show_docs")  # Redirect to prevent resubmission

    documents = Document.objects.all()
    return render(request, "index.html", {"documents": documents})

def upload_document(request):
    if request.method == "POST":
        file = request.FILES.get("file")  # Get single file
        file_path = os.path.join(settings.MEDIA_ROOT, "documents", file.name)

        # Save file locally
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Classify & extract
        category, metadata, summary = classify_and_extract(file_path)

        # Save in DB
        doc = Document(file=file, category=category, summary=summary, metadata=metadata)
        doc.save()
        
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        return JsonResponse({"message": "File uploaded successfully!"}, status=200)

    return render(request, "upload.html")


    

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})
