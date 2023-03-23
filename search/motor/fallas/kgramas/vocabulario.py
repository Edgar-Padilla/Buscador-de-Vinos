import re
#Preprocesamiento
with open("corpusChistes.txt","r") as f:
    texto=f.read()

#Eliminar signos de puntuacion
texto = re.sub(r'[^\w\s]', ' ', texto)
#Eliminar acentos
texto = re.sub(r'[áéíóú]', 'a', texto)
#Eliminar guines bajo y guines normales
texto= re.sub(r'[_-]', ' ', texto)
#Eliminar numeros
texto = re.sub(r'\d', '', texto)
#convertir a minuscular
texto=texto.lower()
#Crear lista de palabras
vocabulario=texto.split()
#Elimanr palabras repetidas haciendo un conjunto de palabras
vocabulario=set(vocabulario)
#ordenar alfabeticamente
vocabulario=sorted(vocabulario)
with open("vocabulario.txt", "w") as f:
    for palabra in vocabulario:
        f.write(palabra + "\n")
vocabulario=["$"+palabra+"$" for palabra in vocabulario]
with open("dollar_vocabulario.txt", "w") as f:
    for palabra in vocabulario:
        f.write(palabra + "\n")
