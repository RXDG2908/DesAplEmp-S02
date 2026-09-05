# biblioteca/views.py
# CRUD completo (Ejercicios 14-17) para las cinco entidades, usando las
# Class-Based Views genéricas de Django (ListView/CreateView/UpdateView/
# DeleteView). Todas usan el ORM de Django; ninguna escribe SQL a mano.

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Bibliotecario, Categoria, Editorial, Libro, Socio

# --- Bibliotecario (independiente) --------------------------------------


class BibliotecarioListView(ListView):
    model = Bibliotecario
    template_name = 'biblioteca/bibliotecario_list.html'
    context_object_name = 'objetos'


class BibliotecarioCreateView(CreateView):
    model = Bibliotecario
    fields = ['nombre', 'dni', 'turno']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:bibliotecario_list')
    extra_context = {'titulo': 'Registrar bibliotecario'}


class BibliotecarioUpdateView(UpdateView):
    model = Bibliotecario
    fields = ['nombre', 'dni', 'turno']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:bibliotecario_list')
    extra_context = {'titulo': 'Editar bibliotecario'}


class BibliotecarioDeleteView(DeleteView):
    model = Bibliotecario
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:bibliotecario_list')


# --- Editorial (independiente) ------------------------------------------


class EditorialListView(ListView):
    model = Editorial
    template_name = 'biblioteca/editorial_list.html'
    context_object_name = 'objetos'


class EditorialCreateView(CreateView):
    model = Editorial
    fields = ['nombre', 'pais']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:editorial_list')
    extra_context = {'titulo': 'Registrar editorial'}


class EditorialUpdateView(UpdateView):
    model = Editorial
    fields = ['nombre', 'pais']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:editorial_list')
    extra_context = {'titulo': 'Editar editorial'}


class EditorialDeleteView(DeleteView):
    model = Editorial
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:editorial_list')


# --- Socio (independiente) ----------------------------------------------


class SocioListView(ListView):
    model = Socio
    template_name = 'biblioteca/socio_list.html'
    context_object_name = 'objetos'


class SocioCreateView(CreateView):
    model = Socio
    fields = ['nombre', 'dni', 'telefono']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:socio_list')
    extra_context = {'titulo': 'Registrar socio'}


class SocioUpdateView(UpdateView):
    model = Socio
    fields = ['nombre', 'dni', 'telefono']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:socio_list')
    extra_context = {'titulo': 'Editar socio'}


class SocioDeleteView(DeleteView):
    model = Socio
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:socio_list')


# --- Categoria (lado "1" de la relación FK) ------------------------------


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'biblioteca/categoria_list.html'
    context_object_name = 'objetos'


class CategoriaCreateView(CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:categoria_list')
    extra_context = {'titulo': 'Registrar categoría'}


class CategoriaUpdateView(UpdateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:categoria_list')
    extra_context = {'titulo': 'Editar categoría'}


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:categoria_list')


# --- Libro (lado "N" de la relación FK -> Categoria) ---------------------


class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'
    context_object_name = 'objetos'
    queryset = Libro.objects.select_related('categoria').order_by('titulo')


class LibroCreateView(CreateView):
    model = Libro
    fields = ['titulo', 'autor', 'isbn', 'anio_publicacion', 'categoria']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:libro_list')
    extra_context = {'titulo': 'Registrar libro'}


class LibroUpdateView(UpdateView):
    model = Libro
    fields = ['titulo', 'autor', 'isbn', 'anio_publicacion', 'categoria']
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:libro_list')
    extra_context = {'titulo': 'Editar libro'}


class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:libro_list')
