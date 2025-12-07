
from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookViewSet
from .views import BookList

#configure a router for the viewset
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')


urlpatterns = [
    #route for the ListAPIView
    path('books/', BookList.as_view(), name='book-list'),
    #route for obtaining auth token
    path('api-token/', obtain_auth_token, name='api_token_auth'),
    #route for the ViewSet to include all CRUD operations
    path('', include(router.urls)),  # include the router URLs
    
]