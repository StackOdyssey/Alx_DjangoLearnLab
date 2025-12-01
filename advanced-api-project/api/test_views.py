from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITests(APITestCase):
    """
    Unit tests for Book API endpoints.
    Covers CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.client.login(username="tester", password="pass123")

        # Create author and book
        self.author = Author.objects.create(name="Chinua Achebe")
        self.book = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author
        )

    def test_list_books(self):
        """Ensure list endpoint returns books with 200 OK."""
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_retrieve_book(self):
        """Ensure detail endpoint returns correct book."""
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    def test_create_book_authenticated(self):
        """Ensure authenticated user can create a book."""
        url = reverse("book-create")
        data = {"title": "Arrow of God", "publication_year": 1964, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

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


    def test_filter_books_by_author(self):
        """Ensure filtering by author name works."""
        url = reverse("book-list") + f"?author__name={self.author.name}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"], self.author.id)

    def test_search_books(self):
        """Ensure search by title works."""
        url = reverse("book-list") + "?search=Fall"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_order_books(self):
        """Ensure ordering by publication_year works."""
        Book.objects.create(title="No Longer at Ease", publication_year=1960, author=self.author)
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))