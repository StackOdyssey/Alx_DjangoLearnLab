
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()          # Query all Book objects
    serializer_class = BookSerializer      # Use BookSerializer for output
    # new viewset for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] #only logged in users can list

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]       #  only admins can CRUD


# BookList: requires authentication (any logged-in user)
# BookViewSet: restricted to admin users only
# Token endpoint: POST username/password to /auth-token/ to receive a token