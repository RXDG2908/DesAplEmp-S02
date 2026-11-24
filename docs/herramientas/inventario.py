import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # raíz del repositorio
EXCLUIR = {"venv", "node_modules", "__pycache__", "migrations", "assets", "static", "dist"}
TAG = re.compile(r"LAB ?\d+ ?- ?EJ")


def archivos():
    for raiz in ("django_project/src", "frontend/src"):
        for d, ds, fs in os.walk(os.path.join(R, raiz)):
            ds[:] = [x for x in ds if x not in EXCLUIR]
            for f in fs:
                if f.endswith((".py", ".jsx", ".js", ".html", ".css")):
                    yield os.path.join(d, f)


def cabecera(lineas):
    """Devuelve cuántas líneas ocupa el bloque de comentarios inicial."""
    h = 0
    for l in lineas:
        s = l.strip()
        if s.startswith(("#", "//", "{#", "<!--", "/*", "*", "-->", "#}")) or s.startswith("=" * 5):
            h += 1
        else:
            break
    return h


if __name__ == "__main__":
    filas = []
    for p in archivos():
        t = open(p, encoding="utf-8", errors="replace").read().splitlines()
        h = cabecera(t)
        head = "\n".join(t[:h])
        tags = len(TAG.findall(head))
        inl = sum(1 for l in t[h:] if TAG.search(l))
        filas.append((os.path.relpath(p, R).replace("\\", "/"), len(t), "ARCHIVO" in head, tags, inl))
    for p, n, hh, tg, inl in sorted(filas):
        print(f"{'H' if hh else '-'} cab:{tg:2} dentro:{inl:2} lin:{n:4} {p}")
    print(len(filas), "archivos")
