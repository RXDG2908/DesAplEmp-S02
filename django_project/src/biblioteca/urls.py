from django.urls import path

from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('bibliotecarios/', views.BibliotecarioListView.as_view(), name='bibliotecario_list'),
    path('bibliotecarios/nuevo/', views.BibliotecarioCreateView.as_view(), name='bibliotecario_crear'),
    path('bibliotecarios/<int:pk>/editar/', views.BibliotecarioUpdateView.as_view(), name='bibliotecario_editar'),
    path('bibliotecarios/<int:pk>/eliminar/', views.BibliotecarioDeleteView.as_view(), name='bibliotecario_eliminar'),

    path('editoriales/', views.EditorialListView.as_view(), name='editorial_list'),
    path('editoriales/nueva/', views.EditorialCreateView.as_view(), name='editorial_crear'),
    path('editoriales/<int:pk>/editar/', views.EditorialUpdateView.as_view(), name='editorial_editar'),
    path('editoriales/<int:pk>/eliminar/', views.EditorialDeleteView.as_view(), name='editorial_eliminar'),

    path('socios/', views.SocioListView.as_view(), name='socio_list'),
    path('socios/nuevo/', views.SocioCreateView.as_view(), name='socio_crear'),
    path('socios/<int:pk>/editar/', views.SocioUpdateView.as_view(), name='socio_editar'),
    path('socios/<int:pk>/eliminar/', views.SocioDeleteView.as_view(), name='socio_eliminar'),

    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_eliminar'),

    path('libros/', views.LibroListView.as_view(), name='libro_list'),
    path('libros/nuevo/', views.LibroCreateView.as_view(), name='libro_crear'),
    path('libros/<int:pk>/editar/', views.LibroUpdateView.as_view(), name='libro_editar'),
    path('libros/<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='libro_eliminar'),
]
