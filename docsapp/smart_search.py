from django.db import connection
from .models import Document

def smart_search(query):
    # Step 1: Try finding an exact match in metadata["Name"] (if applicable)
    exact_match = Document.objects.filter(metadata__Name__icontains=query)

    if exact_match.exists():
        return exact_match

    # Step 2: Use Full-Text Search on the `summary` field via `document_fts`
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT doc_id FROM document_fts WHERE summary MATCH ? ORDER BY rank DESC", [query]
        )
        result_ids = [row[0] for row in cursor.fetchall()]

    # Fetch the matching Document objects
    return Document.objects.filter(id__in=result_ids)
