
from django.db import models

class Author(models.Model):
    """
    Author model:
    - Represents a book author.
    - One author can have many books (one-to-many relationship).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    - Represents a book written by an author.
    - Fields: title, publication_year, and a foreign key to Author.
    - Each book belongs to exactly one author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"