# Apuntes previos — Semanas 1 a 4 (base para el Laboratorio 5)

Curso: **Desarrollo de Aplicaciones Empresariales** — 4 - C24 - Sección CD.
Fuente: PPT y GLAB de cada semana (`cursos/Desarrollo de Aplicaciones
Empresariales [73524]/material/`).

| Archivo | Semana | Tema |
|---|---|---|
| [TEMA_01_Fundamentos_Django.md](TEMA_01_Fundamentos_Django.md) | 1 | Qué es Django, Project vs App, entorno virtual, primer proyecto (`config`/`core`), primer `admin.site.register()` |
| [TEMA_02_MVT_URLs_Views_Templates.md](TEMA_02_MVT_URLs_Views_Templates.md) | 2 | Arquitectura MVT vs MVC, URLs, Views, Templates, Context, `forms.Form` sin base de datos |
| [TEMA_03_ORM_Migraciones_CRUD.md](TEMA_03_ORM_Migraciones_CRUD.md) | 3 | Manager/QuerySets, `makemigrations`/`migrate`, CRUD vía ORM, Post/Redirect/Get, SQLite |
| [TEMA_04_Relaciones_Models.md](TEMA_04_Relaciones_Models.md) | 4 | `OneToOneField`, `ForeignKey`, `ManyToManyField` con `through`, `select_related`/`prefetch_related`, relaciones ya implementadas en `biblioteca` y `vet` |

## Por qué importan para el Laboratorio 5

El Laboratorio 5 (Django Admin) **no agrega modelos ni relaciones nuevas**:
reutiliza exactamente lo construido en las Semanas 1-4.

- **Tema 1** → ya se usó `admin.site.register()` una vez (Lab. 1, modelo
  `Item`); la Semana 5 lo retoma y lo profundiza.
- **Tema 4** → es la base directa: las relaciones 1:1, 1:N y N:M que ya
  existen en `biblioteca` (`CarnetSocio`, `Categoria`→`Libro`, `Prestamo`) y
  en `vet` (`FichaClinica`, `Veterinario`→`Cita`, `ConsumoInsumo`) son las
  que hay que **registrar y personalizar** con `ModelAdmin`, `list_display`,
  `search_fields`, `list_filter`, `StackedInline` (1:1) y `TabularInline`
  (N:M con `through`).
- **Temas 2 y 3** dan el contexto de por qué el Admin "no reemplaza al Model
  ni al ORM: los reutiliza" (pregunta que pide justificar el Ejercicio 8 del
  Laboratorio 5).

Ver el enunciado completo del laboratorio actual en el resumen ya compartido
en la conversación (Guía `GLAB-S05-YBESTARD-2026-02.docx`).
