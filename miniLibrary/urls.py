from django.http import HttpResponseRedirect
from django.views import generic
from django.conf import settings 
from django.conf.urls.static import static

from django.urls import path, include

from miniLibrary.views import BookDetail, UserCreate, LoginView, BookCreate, BookUpdate, BookDelete, CartView, OrderView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #/mini
    path('books/', views.index, name='index'),
    # ex: /miniLibrary/books/5/
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('books/user/registration/', UserCreate.as_view(), name='user-register'),
    path("books/add/", BookCreate.as_view(), name='book-add'),
    path("books/<int:pk>/update/", BookUpdate.as_view(), name='book-update'),
    path("books/<int:pk>/delete/", BookDelete.as_view(), name='book-delete'),
    path('books/<int:book_id>/upload/', views.upload_file, name='image-upload'),
    path('books/login/',LoginView.as_view(), name = 'login-view' ),
    path('books/<int:book_id>/add/',views.addToCart, name = 'login-view' ),
    path('books/cart/',CartView.as_view(), name = 'cart-view' ),
    path('books/order/',OrderView.as_view(), name = 'order-view' ),
    path('books/logout',views.logout, name='logout')
]
