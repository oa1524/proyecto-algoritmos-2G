import json
from classes import *

class App():
    def start(self):
        lista_municipios = self.read()
        self.ver_coord(lista_municipios)

    def read(self):
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

    def ver_coord(self, list_municipios):
        for municipio in list_municipios:
            cant_local = 0
            cant_local_coord = 0
            cant_local_nocoord = 0
            for localidad in municipio.local:
                cant_local+=1
                if localidad.lat and localidad.long != None:
                    cant_local_coord+=1
                else:
                    cant_local_nocoord+=1
            porcentaje_local_coord = (cant_local_coord / cant_local)*100
            print(f"""{"-"*30}
    Municipio: {municipio.nombre}
        Cantidad de localidades cargadas: {cant_local}
        Cantidad de localidades con coordenadas geograficas: {cant_local_coord}
        Cantidad de localidades sin coordenadas geograficas: {cant_local_nocoord}
        Porcentaje de localidades con coordenadas: {round(porcentaje_local_coord, 2)}%
    """)