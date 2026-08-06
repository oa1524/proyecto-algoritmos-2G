import json
from classes import *

'''
Funcion read hecha para leer zonas_caracas.json y organizar su data creando los objetos que le
correspondan respectivamente. 
Esta funcion se coloco posteriormentet en App.py para mayor orden.
'''
def read():
    with open("zonas_caracas.json", "r", encoding="utf-8") as z:
        zonas = json.load(z)

    lista_municipios = []
    for municipio in zonas:
        lista_localidades_obj = []
        lista_localidades = zonas[municipio]
        for localidad in lista_localidades:
            localidad_obj = Localidad(localidad["localidad"], localidad["latitud"], localidad["longitud"])
            lista_localidades_obj.append(localidad_obj)
        municipio_obj = Municipio(municipio, lista_localidades_obj)
        lista_municipios.append(municipio_obj)
    return lista_municipios

