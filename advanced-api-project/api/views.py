from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from .models import Book
from .serializers import BookSerializer
import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author

class BookListView(generics.ListAPIView):
    """
    BookListView:
    - Retrieves all books.
    - Accessible to both authenticated and unauthenticated users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # anyone can view
 # Advanced query capabilities
    filter_backends = [
        filters.DjangoFilterBackend,   
        SearchFilter,                 
        OrderingFilter,                
    ]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    BookDetailView:
    - Retrieves a single book by ID.
    - Accessible to both authenticated and unauthenticated users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    BookCreateView:
    - Allows authenticated users to add a new book.
    - Includes validation to prevent future publication years.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom hook: validate publication_year before saving
        pub_year = serializer.validated_data.get("publication_year")
        current_year = datetime.date.today().year
        if pub_year > current_year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    BookUpdateView:
    - Allows authenticated users to update an existing book.
    - Includes validation to prevent future publication years.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        pub_year = serializer.validated_data.get("publication_year")
        current_year = datetime.date.today().year
        if pub_year > current_year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    BookDeleteView:
    - Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

def test_update_book_authenticated(self):
    """Ensure authenticated user can update a book."""
    url = reverse("book-update", args=[self.book.id])   # ✅ pass pk
    data = {
        "title": "Updated Title",
        "publication_year": 1958,
        "author": self.author.id,
    }
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book.refresh_from_db()
    self.assertEqual(self.book.title, "Updated Title")

def test_delete_book_authenticated(self):
    """Ensure authenticated user can delete a book."""
    url = reverse("book-delete", args=[self.book.id])   # ✅ pass pk
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Book.objects.count(), 0)