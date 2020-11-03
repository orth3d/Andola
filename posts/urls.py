from django.urls import path
from .views import indexBlog, blog, PostCreateView, post_delete, CategoryView, AuthorView, PostDetailView, PostUpdateView #, post_update, post_detail, post_create

urlpatterns = [
    path('', indexBlog),
    path('entradas', blog, name='lista-entradas'),
    # path('create/', post_create, name='post_create'),
    path('post/<pk>/', PostDetailView.as_view(), name='post_detail'),
    # path('post/<id>', post_detail, name='post_detail'),
    # path('post/<id>/update/', post_update, name='post_update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<pk>/delete/', post_delete, name='post_delete'),
    path('category/<int:cats>/', CategoryView, name='category'),
    path('author/<str:auth>/', AuthorView, name='author'),
]
