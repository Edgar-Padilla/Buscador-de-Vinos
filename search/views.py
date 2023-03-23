from django.shortcuts import render
import re
from search.motor.busqueda import busqueda
from search.motor.busquedaAvanza import busquedaAvanzada
from search.globals import frecPosList,vocabulario, doc, posList, dicSinonimos, sinoExpanDic, bigramDic, tree, invTree, totalDocuments
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tipo(entrada):
    expresion_regular = r"[*]|NOT|AND|OR"
    if re.search(expresion_regular, entrada):
        return False
    else:
        return True
def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        if tipo(search):
            print("busqueda normal")
            b=busqueda(frecPosList,vocabulario, doc, posList, dicSinonimos, sinoExpanDic, bigramDic)
            final_result =b.identificar(search)
        else:
            print("busqueda avanzada")
            b=busquedaAvanzada(frecPosList, vocabulario, doc, posList, dicSinonimos, sinoExpanDic, bigramDic, tree, invTree, totalDocuments)
            final_result =b.buscador(search)
        context = {
            'final_result': final_result
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')