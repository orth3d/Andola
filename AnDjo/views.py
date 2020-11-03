from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import  TemplateView #, ListView, DetailView, View
from django.core.mail import send_mail
from posts.models import Post


class IndexView(TemplateView):
    template_name = 'index.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    featured = Post.objects.filter(featured=True)
    featured = featured.order_by('-timestamp')[:2]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent, 'object_list': self.featured,}
        return context

class ServiciosView(TemplateView):
    template_name = 'servicios.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context
    

class AcupunturaView(TemplateView):
    template_name = 'acupuntura.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context

class QuiropracticaView(TemplateView):
    template_name = 'quiropractica.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context

class PsicologiaView(TemplateView):
    template_name = 'psicologia.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context

class RehabilitacionView(TemplateView):
    template_name = 'rehabilitacion.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context

class NosotrosView(TemplateView):
    template_name = 'nosotros.html'
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'most_recent': self.most_recent}
        return context

def contacto(request):
    most_recent = Post.objects.order_by('-timestamp')[:3]
    
    context = {
        'most_recent': most_recent,
    }

    if request.method == "POST":
        name = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        mensaje = request.POST['mensaje']
        # send email
        send_mail(
            name + ' intenta contactarte',
            name + ' ha dejado este mensaje en andola.com: ' + mensaje + ' ' + telefono + ' ' + email,
            email,
            ['andola.saludintegral@gmail.com'],
        )
        context.update({'name': name})
        return render(request, 'contacto.html', context)

    
    else:
        return render(request, 'contacto.html', context)
