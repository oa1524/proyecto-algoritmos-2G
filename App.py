import json
from classes import *
import requests
from datetime import datetime
from dicc_wmo import WEATHER_CODES
import pandas as pd
import matplotlib as plt

class App():
    lista_municipios = []
    lista_registro = []

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
                if localidad.lat is not None and localidad.long is not None:
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
                                lista_municipios_filt = []
                                for localidad in municipio_selecc.local:
                                    if localidad.lat is not None and localidad.long is not None:
                                        num_opcion2 += 1
                                        print(f"{num_opcion2}. {localidad.local}")
                                        lista_municipios_filt.append(localidad)
                                opcion1_1_local = int(input("Seleccione una opcion: "))

                                if opcion1_1_local == 0:
                                    break
                                elif not (opcion1_1_local > 0 and opcion1_1_local <= num_opcion2):
                                    print("Opcion invalida.")
                                    continue
                                else: 
                                    localidad_selecc = lista_municipios_filt[opcion1_1_local -1]
                                    temperatura_localidad = self.consulta_api(municipio_selecc.nombre, localidad_selecc.local, localidad_selecc.lat, localidad_selecc.long)
                                    self.registrar_consulta(municipio_selecc.nombre, localidad_selecc.local, temperatura_localidad)
                                    
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
                                    temperatura_localidad = self.consulta_api(municipio.nombre, localidad.local, localidad.lat, localidad.long)
                                    self.registrar_consulta(municipio.nombre, localidad.local, temperatura_localidad)
                                    encontrado = True
                                    break
                        if not encontrado:
                            print("Opcion invalida. No se encontro coincidencias.")
            else:
                print("Opcion invalida.")
                continue

    def consulta_api(self, municipio, localidad, latitud, longitud):
        if latitud is None or longitud is None:
            print("No se posee datos de latitud y longitud.")
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=America%2FNew_York&forecast_days=1"
            consulta = requests.get(url)
            dicc = consulta.json()
            wmo = dicc['current']['weather_code']
            time = dicc['current']['time']
            hora_actual = datetime.fromisoformat(time).time()
            fecha_actual = datetime.fromisoformat(time).date()
            print(f"""{"-"*30}
Fecha: {fecha_actual}
Hora: {hora_actual}
Nombre de municipio: {municipio}
Nombre de localidad: {localidad}
Latitud: {latitud}
Longitud: {longitud}
Temperatura actual: {dicc['current']['temperature_2m']}°C
Humedad relativa: {dicc['current']['relative_humidity_2m']}%
Velocidad del viento: {dicc['current']['wind_speed_10m']} km/h
Estado del tiempo: {WEATHER_CODES[wmo]}
    """)
            return dicc['current']['temperature_2m']

    
    def menu2(self):
        while True:
            print(f"""{"-"*30} 
Reportes y estadisticas:
0. Volver al menu anterior
1. Consultar ranking de temperaturas
2. Cobertura geografica
3. Promedio general""")

            opcion2= input('Seleccione una opcion:')

            if opcion2 == "0":
                break
            elif opcion2== "1":
                self.ranking_temperatura ()
            elif opcion2== "2":
                self.cobertura_geografica()
            elif opcion2 == "3":
                self.promedio_temperaturas()
            else:
                print("Opcion invalida. Escriba un numero del 0-3")
                self.menu2()


    def ranking_temperatura (self):
     print (f'{"-"*30} \n Comparacion de temperaturas consultadas ')
 
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
     print (f'Mas fria: {mas_fria.municipio, mas_fria.localidad} con {mas_fria.temperatura} grados c')


    def cobertura_geografica(self):
        print(f"""{"-"*30} \n Localidades sin coordenadas""")

        for municipio in self.lista_municipios:
            sin_coordenadas=[]
            for localidad in municipio.local:
                if localidad.lat is None or localidad.long is None:
                    sin_coordenadas.append(localidad.local)
            if len(sin_coordenadas) >0:
                print (f"{'-'*30}\nMunicipio:{municipio.nombre}")
                for nombre_loc in sin_coordenadas:
                    print (f"- {nombre_loc}")

    def registrar_consulta (self, municipio, localidad, temperatura):
        nuevo_registro = RegistroConsulta(municipio, localidad, temperatura)
        self.lista_registro.append(nuevo_registro)

    def promedio_temperaturas(self):
        print(f'''{'-'*30}\n Promedio de temperaturas consultadas''')
        cant_registros=len(self.lista_registro)
        if cant_registros==0:
            print('No se puede realizar el promedio ya que no hay consultas')
            return
        datos= [
            {
              'municipio': reg.municipio,
              'localidad': reg.localidad,
              'temperatura': reg.temperatura
             }
             for reg in self.lista_registro
          ]
        df=pd.DataFrame(datos)
        promedio= df['temperatura'].mean()
        print(f'Total de consultas realizadas: {len(df)}')
        print(f'Promedio de temperatura: {promedio:.2f} grados c')

    def menu3(self):
        print(f"""{"-"*30}
Historicos:
0. Volver al menu anterior
1. Consulta por periodo de tiempo """)
        opcion3=input('Seleccione una opcion: ')
        if opcion3 =='0':
            self.menu_p
        elif opcion3=='1':
           opcion4=input('Escriba el nombre de la localidad: ').lower().strip()
           localidad_hallada=None
           for municipio in  self.lista_municipios:
               for loc in municipio.local:
                   if opcion4 in loc.local.upper():
                       localidad_hallada=loc
                       break
               if localidad_hallada:
                   break
           if localidad_hallada is None:
               print ('Localidad no encontrada')
           else:
             print(f'Localidad hallada: {localidad_hallada.local}')
             fecha_inicio=input('Ingrese fecha de inicio (AAAA-MM-DD): ')
             fecha_fin=input('Ingrese fecha de fin (AAAA-MM-DD): ')
             df_datos= self.obtener_historicos_api(localidad_hallada.lat, localidad_hallada.long, fecha_inicio, fecha_fin)
             self.procesar_historicos(localidad_hallada.local, df_datos)
                
        else:
            print('Opcion no valida')
            self.menu3

    def obtener_historicos_api(self, lat, long, fecha_inicio, fecha_fin):
        url=f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={fecha_inicio}&end_date={fecha_fin}&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max&timezone=auto"
        res= requests.get(url)
        datos= res.json()

        df= pd.DataFrame(datos['daily'])
        df['time']= pd.to_datetime(df["time"])

        #renombrar las columnas para no usar los nombres largos que da la API

        df= pd.rename(columns={
            'temperature_2m_mean':'temperatura',
            'relative_humidity_2m_mean': 'humedad',
            'precipitacion_sum':'precipitacion',
            'wind_speed_10m_max': 'viento'
        })

        return df 

    def procesar_historicos(self, localidad_nombre, df):
        df['anio']=df['time'].dt.year
        df['anio_mes']=df['time'].dt.strftime('%Y-%m')


        print(f'''{'-'*30} Datos mensuales historicos: {localidad_nombre}''')
        meses_unicos=df['mes'].unique()
        for m in meses_unicos:
            df_mes=df[df['mes']==m]
            print(f''' Mes: {m}
Temperatura promedio: {df_mes['temperatura'].mean():.2f} grados c
Humedad relativa promedio: {df_mes['humedad'].mean():.2f} %
Precipitacion acomulada promedio: {df_mes['precipitacion'].sum():.2f} mm
Velocidad del viento promedio: {df_mes['viento'].mean():.2f} km/h ''')

        print(f'''{'-'*30} Promedios generales del periodo
Temperatura media: {df['temperatura'].mean():.2f}) grados c
Humedad relativa media: {df['humedad'].mean():.2f} %
Precipitacion media diaria: {df['precipitacion'].mean():.2f} mm
Velocidad del viento media: {df['temperatura'].mean():.2f} km/h''')
        