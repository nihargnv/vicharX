"""
URL configuration for aiFileManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', show_docs, name='show_docs'),
    path('upload/', upload_document, name='upload_document'),
    path('documents/', document_list, name='document_list'),
    path("api/documents/", get_documents, name="get_documents"),
    path("document_search/", smart_search_view, name="smart_search"),
    path("document/<int:doc_id>/", document_details, name="document_details"),
    path('document/<int:document_id>/delete/', delete_document, name='delete_document'),
    path("search/", search_documents, name="search_documents"),
    path('document/<int:document_id>/', document_view, name='document_view'),
    path('document/<int:document_id>/download/', document_download, name='document_download'),
    path("analytics/", analytics_view, name="analytics"),
]
