# Views file for the blog App
# import json
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from marketing.models import Signup
from .forms import  PostForm 
from .models import Post, Author, PostView, Category

# Create your views here.

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__pk', 'categories__categoria') \
        .annotate(Count('categories__categoria'))
    return queryset

def indexBlog(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    most_recent = Post.objects.order_by('-timestamp')[:3]
    catego = featured.values()

    context = {
        'catego': catego,
        'object_list': featured,
        'latest': latest,
        'most_recent': most_recent,
    }

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        context.update({'email': email})
        return render(request, 'blog/index_blog.html', context)

    else:
        return render(request, 'blog/index_blog.html', context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog/blog.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        return context

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('BlogListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                form.instance.author = get_author(self.request.user)
                data = form.save(commit=False)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear nueva Entrada'
        context['entity'] = 'Posts'
        context['list_url'] = reverse_lazy('BlogListView')
        context['action'] = 'add'
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('BlogListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Entrada'
        context['entity'] = 'Posts'
        context['list_url'] = reverse_lazy('BlogListView')
        context['action'] = 'edit'
        return context

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'gestion/post_delete.html'
    success_url = reverse_lazy('BlogListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Entrada'
        context['entity'] = 'Posts'
        context['list_url'] = reverse_lazy('BlogListView')
        return context


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect(reverse("lista-entradas"))

def CategoryView(request, cats):
    category_posts = Post.objects.filter(categories=cats)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    qs = category_posts.values()
    category_name = Category.objects.filter(pk=cats)
    
    context = {
        'catego': category_name,
        'queryset': qs,
        'cats': cats,
        'category_posts': category_posts,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'blog/category.html', context)

def AuthorView(request, auth):
    author_posts = Post.objects.filter(author=auth)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    qs = Author.objects.filter(pk=auth)
  
    context = {
        'queryset': qs,
        'auth': auth,
        'author_posts': author_posts,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'blog/author.html', context)
