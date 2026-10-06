# biblioteca/views.py
# CRUD completo (Ejercicios 14-17) para las cinco entidades, usando las
# Class-Based Views genéricas de Django (ListView/CreateView/UpdateView/
# DeleteView). Todas usan el ORM de Django; ninguna escribe SQL a mano.

from datetime import date, timedelta

from django.db import transaction
from django.db.models import Count, F, Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import PrestarForm
from .models import (Bibliotecario, CarnetSocio, Categoria, Editorial,
                     Libro, Prestamo, Socio)

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
    # Ejercicio 12: select_related resuelve la FK; prefetch_related recorre
    # el modelo intermedio Prestamo y llega hasta el Socio.
    queryset = (Libro.objects
                .select_related('categoria')
                .prefetch_related('prestamos__socio')
                .order_by('titulo'))


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


# --- Semana 4 ------------------------------------------------------------
# Ejercicio 12: vista que muestra datos RELACIONADOS (no un listado plano).


class SocioDetailView(DetailView):
    """Muestra el 1:1 (carnet) y el recorrido del modelo intermedio."""
    model = Socio
    template_name = 'biblioteca/socio_detail.html'
    context_object_name = 'socio'
    # select_related() tambien funciona sobre el 1:1 INVERSO ('carnet').
    queryset = (Socio.objects
                .select_related('carnet')
                .prefetch_related('prestamos__libro__categoria'))


# Ejercicio 13: CRUD propio del modelo intermedio Prestamo.

_PRESTAMO_FIELDS = ['socio', 'libro', 'fecha_prestamo',
                    'fecha_devolucion_prevista', 'fecha_devolucion_real',
                    'estado']


class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'biblioteca/prestamo_list.html'
    context_object_name = 'objetos'
    queryset = Prestamo.objects.select_related('socio', 'libro')
    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.GET.get('estado')
        if estado:
            qs = qs.con_estado(estado)
        return qs


class PrestamoCreateView(CreateView):
    model = Prestamo
    fields = _PRESTAMO_FIELDS
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:prestamo_list')
    extra_context = {'titulo': 'Registrar préstamo'}


class PrestamoUpdateView(UpdateView):
    model = Prestamo
    fields = _PRESTAMO_FIELDS
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:prestamo_list')
    extra_context = {'titulo': 'Editar préstamo'}


class PrestamoDeleteView(DeleteView):
    model = Prestamo
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:prestamo_list')


# CRUD del carnet (1:1), necesario para poder crearlo desde la web.

_CARNET_FIELDS = ['socio', 'codigo', 'fecha_emision', 'fecha_vencimiento',
                  'vigente']


class CarnetListView(ListView):
    model = CarnetSocio
    template_name = 'biblioteca/carnet_list.html'
    context_object_name = 'objetos'
    queryset = CarnetSocio.objects.select_related('socio')


class CarnetCreateView(CreateView):
    model = CarnetSocio
    fields = _CARNET_FIELDS
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:carnet_list')
    extra_context = {'titulo': 'Emitir carnet'}


class CarnetUpdateView(UpdateView):
    model = CarnetSocio
    fields = _CARNET_FIELDS
    template_name = 'biblioteca/generic_form.html'
    success_url = reverse_lazy('biblioteca:carnet_list')
    extra_context = {'titulo': 'Editar carnet'}


class CarnetDeleteView(DeleteView):
    model = CarnetSocio
    template_name = 'biblioteca/generic_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:carnet_list')

def prestamo_registrar(request):
    error = None
    if request.method == 'POST':
        form = PrestarForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            hoy = date.today()
            try:
                with transaction.atomic():
                    Prestamo.objects.create(
                        socio=datos['socio'],
                        libro=datos['libro'],
                        fecha_prestamo=hoy,
                        fecha_devolucion_prevista=hoy + timedelta(days=datos['dias']),
                        estado='Activo',
                    )
                    filas = Libro.objects.filter(
                        pk=datos['libro'].pk,
                        copias__gte=1,
                    ).update(copias=F('copias') - 1)
                    if filas == 0:
                        raise ValueError('No hay copias disponibles de ' + datos['libro'].titulo)
            except ValueError as e:
                error = str(e)
            else:
                return redirect('biblioteca:socio_detail', pk=datos['socio'].pk)
    else:
        form = PrestarForm()
    return render(request, 'biblioteca/prestamo_registrar.html', {'form': form, 'error': error})

def reporte(request):
    total_multas = Prestamo.objects.aggregate(total=Sum('multa'))['total']
    por_libro = Libro.objects.annotate(n=Count('prestamos')).order_by('-n')
    por_estado = (Prestamo.objects.values('estado')
                  .annotate(total=Count('id'), multas=Sum('multa'))
                  .order_by('-total'))
    atrasados_con_multa = Prestamo.objects.con_estado('Atrasado').con_multa().count()
    return render(request, 'biblioteca/reporte.html', {
        'total_multas': total_multas,
        'por_libro': por_libro,
        'por_estado': por_estado,
        'atrasados_con_multa': atrasados_con_multa,
    })