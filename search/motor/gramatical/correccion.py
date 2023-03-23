import json
class correccionGramatical:
    def __init__(self):
        self.matrizTransicion={}
        with open('search/motor/files/matrizTransicion.txt','r') as f:
            self.matrizTransicion = json.load(f)
    def correcion(self,oracion, umbral_probabilidad=0.8):
        palabras = oracion.split()
        correccion = []
        for i, palabra in enumerate(palabras):
            # Calcular la probabilidad condicional de la palabra dada la palabra anterior
            if i == 0:
                probabilidad_condicional = 1.0  # Si es la primera palabra, la probabilidad es 1
            else:
                palabraAnterior = palabras[i-1]
                probabilidad_condicional = self.matrizTransicion[palabra][palabraAnterior]
            # Reemplazar palabras improbables
            if probabilidad_condicional < umbral_probabilidad:
                palabras_posibles = self.matrizTransicion.get(palabraAnterior, {})
                palabra_corregida = max(palabras_posibles, key=palabras_posibles.get, default=palabra)
                correccion.append(palabra_corregida)
                #print(palabra)
                #print(palabraAnterior)
                #print(palabras_posibles)
                #print(palabra_corregida)
            else:
                correccion.append(palabra)
        return ' '.join(correccion)

    def main(self):
        oracion="habia una voz"
        print(self.correcion(oracion))
run=correccionGramatical()
run.main()