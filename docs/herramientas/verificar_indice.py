"""Comprueba que cada línea del índice apunte a su ejercicio.
Uso: python docs/herramientas/verificar_indice.py
"""
import os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
from inventario import archivos, R
from indice_ejercicios import ANCLAS, MARCA, expandir, TITULO, LUCAS
mal=0; total=0
for p in archivos():
    rel=os.path.relpath(p,R).replace("\\","/")
    if any(k in rel for k in LUCAS): continue
    L=open(p,encoding='utf-8').read().split("\n")
    if not any(TITULO in l for l in L): continue
    anc=next((v for c,v in ANCLAS.items() if rel.endswith(c)),{})
    for l in L:
        m=re.search(r"LAB (\d+) - EJ (\d+) \.+ líneas? ([\d, ]+)",l)
        if not m: continue
        lab,e=int(m.group(1)),int(m.group(2))
        for n in map(int,m.group(3).split(",")):
            total+=1
            t=L[n-1]
            ok=any(int(a)==lab and e in expandir(b) for a,b in MARCA.findall(t))
            if not ok and f"{lab}-{e}" in anc: ok=bool(re.search(anc[f"{lab}-{e}"],t))
            if not ok: mal+=1; print("MAL",rel,lab,e,n,repr(t[:80]))
print("referencias:",total,"incorrectas:",mal)
