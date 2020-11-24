from django.urls import path
from .views import AddDocumentView, Success, CreateIndexView

urlpatterns = [
    path('', AddDocumentView.as_view(), name='add_document'),
    path('create-index/', CreateIndexView.as_view(), name='create_index'),
    path('success/', Success.as_view(), name='success'),
]