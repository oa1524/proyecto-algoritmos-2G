import json
from classes import *

class App():
    lista_municipios = []

    def start(self):
        self.read()
        self.ver_coord()
        self.menu_p()

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

    def menu_p(self):
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
            elif opcion == 1:
                self.menu1()
            elif opcion == 2:
                self.menu2()
            elif opcion == 3:
                self.menu3()
            else:
                print("Opcion invalida.")
                continue


    def menu1(self):
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
            elif opcion1_1 == 1:
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
                            while True:
                                print(F"""{"-"*30}
0. Volver al menu anterior
Municipio seleccionado: {municipio_selecc.nombre}""")
                                num_opcion2 = 0
                                for localidad in municipio_selecc.local:
                                    if localidad.lat and localidad.long != None:
                                        num_opcion2 += 1
                                        print(f"{num_opcion2}. {localidad.local}")
                                opcion1_1_local = int(input("Seleccione una opcion: "))
                                if opcion1_1_local == 0:
                                    break
                                elif not (opcion1_1_local > 0 and opcion1_1_local <= num_opcion2):
                                    print("Opcion invalida.")
                                    continue
                                else: 
                                    localidad_selecc = municipio_selecc.local[opcion1_1_local -1]
                                    # CONTINUAR
            elif opcion1_1 == 2:
                while True:
                    encontrado = False
                    print("-"*30)
                    opcion1_2 = input("Escriba la localidad a buscar (Si desea volver al menu anterior ingrese '0'): ").strip().upper()
                    if opcion1_2 == "0":
                        break
                    elif len(opcion1_2) < 3:
                        print("Opcion invalida. Escriba tres o mas caracteres.")       
                    else:
                        for municipio in self.lista_municipios:
                            if encontrado:
                                break
                            for localidad in municipio.local:
                                if opcion1_2 in localidad.local.upper(): 
                                    print(f"""Municipio seleccionado: {municipio.nombre}
Localidad seleccionada: {localidad.local}""")
                                    # CONSULTAR API
                                    encontrado = True
                                    break
                        if not encontrado:
                            print("Opcion invalida. No se encontro coincidencias.")
            else:
                print("Opcion invalida.")
                continue

    lista_registro = []
    nuevo_registro = RegistroConsulta
    lista_registro.append (nuevo_registro)

    def ranking_temperatura (self):
        print (f'{"-"*30} \n "Comparacion de temperaturas consultadas" \n {"-"*30}')

        if len(self.lista_registro)==0:
           print ('No se puede realizar la comparacion ya que no se ha buscado nada')
           return

        mas_calida = self.lista_registro[0]
        mas_fria = self.lista_registro[0]

        for registro in self.lista_registro:
            if registro.temperatura > mas_calida.temperatura:
                mas_calida = registro

            if registro.temperatura < mas_fria.temperatura:
                mas_fria = registro

        print (f'Mas calida: {mas_calida.municipio, mas_calida.localidad} con {mas_calida.temperatura} grados c')
        print (f'Mas fria: {mas_fria.municipio, mas_fria.localidad} con {mas_fria.temepratura} grados c')
                
       