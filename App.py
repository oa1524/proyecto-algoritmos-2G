import json
from classes import *

class App():
    lista_municipios = []

    def start(self):
        self.read()
        self.ver_coord()
        self.menu()

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
        self.lista_municipios = lista_municipios

    def ver_coord(self):
        for municipio in self.lista_municipios:
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

    def menu(self):
        while True:
            print(f"""{"-"*30}
0. Cerrar programa
1. Consulta del clima en tiempo real
2. Reportes y Estadisticas
3. Historicos
""")
            opcion = int(input("Seleccione una opcion: "))
            if opcion == 0:
                break
            if opcion == 1:
                while True:
                    print(f"""{"-"*30}
Consulta del clima en tiempo real:
0. Volver al menu anterior
1. Por municipio y localidad
2. Mediante busqueda directa por nombre de localidad
""")
                    opcion1_1 = int(input("Seleccione una opcion: "))
                    if opcion1_1 == 0:
                        break
                    if opcion1_1 == 1:
                        while True:
                            print(f"""{"-"*30}
0. Volver al menu anterior""")
                            for municipio in self.lista_municipios:
                                num_opcion = self.lista_municipios.index(municipio) +1
                                print(f"{num_opcion}. {municipio.nombre}")
                            opcion1_1_n = int(input("Seleccione una opcion: "))
                            if opcion1_1_n == 0:
                                break
                            elif not (opcion1_1_n > 0 and opcion1_1_n <= len(self.lista_municipios)):
                                print("Opcion invalida.")
                                continue
                            else: 
                                municipio_selecc = self.lista_municipios[opcion1_1_n -1]
                                print("Municipio seleccionado: ", municipio_selecc.nombre)
