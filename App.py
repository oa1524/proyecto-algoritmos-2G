import json
from classes import *
import requests
from dicc_wmo import WEATHER_CODES
import pandas as pd
import matplotlib.pyplot as plt

class App:
    lista_municipios = []
    lista_registro = []


    def start(self):
        '''
        Metodo principal que llama a ejecutar el resto de los metodos de la clase para el
        funcionamiento del programa.
        '''
        self.read()
        self.ver_coord()
        self.menu_p()


    def read(self):
        '''
        Metodo read hecho para leer zonas_caracas.json y organizar su data creando los objetos que le
        correspondan respectivamente. 
        '''
        with open("zonas_caracas.json", "r", encoding="utf-8") as z:
            zonas = json.load(z)
        self.lista_municipios = []
        for municipio in zonas:
            lista_localidades_obj = []
            lista_localidades = zonas[municipio]
            for localidad in lista_localidades:
                localidad_obj = Localidad(localidad["localidad"], localidad["latitud"], localidad["longitud"])
                lista_localidades_obj.append(localidad_obj)
            municipio_obj = Municipio(municipio, lista_localidades_obj)
            self.lista_municipios.append(municipio_obj)


    def ver_coord(self):
        '''
        Metodo utilizado para generar el reporte inicial del programa (Requerimiento 1 Carga de datos)
        '''
        for municipio in self.lista_municipios:
            cant_local = 0
            cant_local_coord = 0
            cant_local_nocoord = 0
            for localidad in municipio.local:
                cant_local+=1
                if localidad.tiene_coordenadas():
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
        '''
        Metodo que genera el menu principal del programa y evalua que opcion selecciona el usuario
        llamando respectivamente al resto de los menus.
        '''
        while True:
            print(f"""{"-"*30}
0. Cerrar programa
1. Consulta del clima en tiempo real
2. Reportes y Estadisticas
3. Historicos
""")
            opcion = input("Seleccione una opcion: ")
            if opcion == "0":
                break
            elif opcion == "1":
                self.menu1()
            elif opcion == "2":
                self.menu2()
            elif opcion == "3":
                self.menu3()
            else:
                print("Opcion invalida.")
                continue

    def menu1(self):
        '''
        Metodo que genera el menu1, el cual realiza todo el Requerimiento 2: Consulta del clima en tiempo real.
            1. Por municipio y localidad: despliegua la lista de municipios, luego sus localidades, segun
        la seleccion del usuario consulta la API e imprime la informacion obtenida, registrando la consulta 
        como un objeto de clase RegistroConsulta.
            2. Mediante busqueda directa por nombre de localidad: el usuario introduce caracteres, si el programa
        encuentra coincidencias, consulta la API e imprime la informacion obtenida, registrando la consulta 
        como un objeto de clase RegistroConsulta.
        '''
        while True:
            print(f"""{"-"*30}
Consulta del clima en tiempo real:
0. Volver al menu anterior
1. Por municipio y localidad
2. Mediante busqueda directa por nombre de localidad
""")
            opcion1_1 = input("Seleccione una opcion: ")
            if opcion1_1 == "0":
                break
            elif opcion1_1 == "1":
                while True:
                    print(f"""{"-"*30}
0. Volver al menu anterior""")
                    for municipio in self.lista_municipios:
                        num_opcion = self.lista_municipios.index(municipio) +1
                        print(f"{num_opcion}. {municipio.nombre}")
                    opcion1_1_n = input("Seleccione una opcion: ")
                    if opcion1_1_n == "0":
                            break
                    elif not opcion1_1_n.isnumeric():
                        print("Opcion invalida.")
                        continue
                    elif not (int(opcion1_1_n) > 0 and int(opcion1_1_n) <= len(self.lista_municipios)):
                            print("Opcion invalida.")
                            continue
                    else: 
                            municipio_selecc = self.lista_municipios[int(opcion1_1_n) -1]
                            while True:
                                print(F"""{"-"*30}
0. Volver al menu anterior
Municipio seleccionado: {municipio_selecc.nombre}""")
                                num_opcion2 = 0
                                lista_municipios_filt = []
                                for localidad in municipio_selecc.local:
                                    if localidad.tiene_coordenadas():
                                        num_opcion2 += 1
                                        print(f"{num_opcion2}. {localidad.local}")
                                        lista_municipios_filt.append(localidad)
                                opcion1_1_local = input("Seleccione una opcion: ")

                                if opcion1_1_local == "0":
                                    break
                                elif not opcion1_1_local.isnumeric():
                                    print("Opcion invalida.")
                                    continue
                                elif not (int(opcion1_1_local) > 0 and int(opcion1_1_local) <= num_opcion2):
                                    print("Opcion invalida.")
                                    continue
                                else: 
                                    localidad_selecc = lista_municipios_filt[int(opcion1_1_local) -1]
                                    temperatura_localidad = self.consulta_api(municipio_selecc.nombre, localidad_selecc.local, localidad_selecc.lat, localidad_selecc.long)
                                    self.registrar_consulta(municipio_selecc, localidad_selecc, temperatura_localidad)
                                    
            elif opcion1_1 == "2":
                while True:
                    print("-"*30)
                    opcion1_2 = input("Escriba la localidad a buscar (Si desea volver al menu anterior ingrese '0'): ").strip().upper()
                    if opcion1_2 == "0":
                        break
                    elif len(opcion1_2) < 3:
                        print("Opcion invalida. Escriba tres o mas caracteres.")       
                    else:
                            numero_opcion = 0
                            coincidencias = []
                            municipio_coincidencias = []
                            for municipio in self.lista_municipios:
                                for localidad in municipio.local:
                                    if opcion1_2.upper() in localidad.local.upper() and localidad.tiene_coordenadas():
                                        numero_opcion += 1
                                        coincidencias.append(localidad)
                                        municipio_coincidencias.append(municipio)
                            if numero_opcion == 0:
                                    print("Opcion invalida. No se encontro coincidencias.")
                            else:
                                    while True: 
                                        print(f'''{'-'*30}
Se encontraron coincidencias, seleccione una opcion. (Si desea volver al menu anterior ingrese '0'): ''')
                                        for localidad in coincidencias:
                                            numero_opcion2 = coincidencias.index(localidad) + 1
                                            print(f'{numero_opcion2}. {localidad.local}')
                                        opcion_coin = input("Seleccione una opcion: ")
                                        if not opcion_coin.isnumeric():
                                            print("Opcion invalida.")
                                            continue
                                        elif opcion_coin == "0":
                                            break
                                        elif not (int(opcion_coin) > 0 and int(opcion_coin) <= numero_opcion):
                                            print("Opcion invalida.")
                                            continue
                                        else:
                                            localidad = coincidencias[int(opcion_coin) - 1]
                                            municipio = municipio_coincidencias[int(opcion_coin) - 1]
                                            temperatura_localidad = self.consulta_api(municipio.nombre, localidad.local, localidad.lat, localidad.long)
                                            self.registrar_consulta(municipio, localidad, temperatura_localidad)
                                            continue
            else:
                print("Opcion invalida.")
                continue


    def consulta_api(self, municipio, localidad, latitud, longitud):
        '''
        Primer metodo de consulta a la API que devuelve e imprime los detalles meteorológicos de la localidad
        consultada por el usuario y colocada con sus especificaciones en los argumentos de este metodo. Tambien,
        devuelve el valor de temperatura para poder ser usado en el menu2. (Reportes y Estadisticas)
        '''
        if latitud is None or longitud is None:
            print("No se posee datos de latitud y longitud.") 
            return None
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=America%2FNew_York&forecast_days=1"
            consulta = requests.get(url)
            dicc = consulta.json()
            wmo = dicc['current']['weather_code']
            print(f"""{"-"*30}
Nombre de municipio: {municipio}
Nombre de localidad: {localidad}
Latitud: {latitud}
Longitud: {longitud}
Temperatura actual: {dicc['current']['temperature_2m']}°C
Humedad relativa: {dicc['current']['relative_humidity_2m']}%
Velocidad del viento: {dicc['current']['wind_speed_10m']} km/h
Estado del tiempo: {WEATHER_CODES[wmo]}""")
            return dicc['current']['temperature_2m']
        
    def menu2(self):
        '''
        Metodo que genera el menu de reportes y estadisticas (opcion 2 del menu principal).
        Permite seleccionar entre consultar ranking de temperaturas, ver la cobertura geografica sin coordenadas o 
        calcular el promedio de las consultas realizadas.
        '''
        while True:
            print(f"""{"-"*30} 
Reportes y estadisticas:
0. Volver al menu anterior
1. Consultar ranking de temperaturas
2. Cobertura geografica
3. Promedio general""")

            opcion2 = input('Seleccione una opcion: ')

            if opcion2 == "0":
                break
            elif opcion2 == "1":
                self.ranking_temperatura ()
            elif opcion2 == "2":
                self.cobertura_geografica()
            elif opcion2 == "3":
                self.promedio_temperaturas()
            else:
                print("Opcion invalida. Escriba un numero del 0-3")
                continue

    
    def ranking_temperatura (self):
        '''
        Metodo encargado de evaluar las consultas realizadas que estan en el historial de registro.
        Determina e imprime la localidad que tiene la temperatura mas fria y la mas calida.
        Si no existen registros previo lo informa.
        '''
        print (f'{"-"*30} \n Comparacion de temperaturas consultadas ')
    
        if len(self.lista_registro) == 0:
            print ('No se puede realizar la comparacion ya que no se ha buscado nada')
            return

        mas_calida = self.lista_registro[0]
        mas_fria = self.lista_registro[0]

        for registro in self.lista_registro:
            if registro.temperatura > mas_calida.temperatura:
                mas_calida = registro
    
            if registro.temperatura < mas_fria.temperatura:
                mas_fria = registro

        print (f'Mas calida: {mas_calida.municipio.nombre, mas_calida.localidad.local} con {mas_calida.temperatura} °C')
        print (f'Mas fria: {mas_fria.municipio.nombre, mas_fria.localidad.local} con {mas_fria.temperatura} °C')

    def cobertura_geografica(self):
        '''
        Metodo que recorre la lista de municipios y sus localidades para identificar las que no poseen coordenadas.
        Imprime en pantalla las localidades sin coordenads ordenadas por municipio.
        '''
        print(f"""{"-"*30} \n Localidades sin coordenadas""")

        for municipio in self.lista_municipios:
            sin_coordenadas = []
            for localidad in municipio.local:
                if localidad.lat is None or localidad.long is None:
                    sin_coordenadas.append(localidad.local)
            if len(sin_coordenadas) > 0:
                print (f"{'-'*30}\nMunicipio:{municipio.nombre}")
                for nombre_loc in sin_coordenadas:
                    print (f"- {nombre_loc}")

    def registrar_consulta (self, municipio, localidad, temperatura):
        '''
        Metodo auxiliar que crea un objeto de la clase registro consulta con los datos de una busqueda y 
        lo guarda en un lista de registro que es usada otras funciones.
        '''
        nuevo_registro = RegistroConsulta(municipio, localidad, temperatura)
        self.lista_registro.append(nuevo_registro)

    def promedio_temperaturas(self):
        '''
        Metodo que procesa el historial de consultas(lista) y lo transforma en un data frame de pandas.
        Calcula e imprime el promedio general de temperaturas obtenidas en la consulta.
        '''
        print(f'''{'-'*30}\n Promedio de temperaturas consultadas''')
        cant_registros = len(self.lista_registro)
        if cant_registros == 0:
            print('No se puede realizar el promedio ya que no hay consultas')
            return
        datos = [
            {
              'municipio': reg.municipio.nombre,
              'localidad': reg.localidad.local,
              'temperatura': reg.temperatura
             }
             for reg in self.lista_registro
          ]
        df = pd.DataFrame(datos)
        promedio = df['temperatura'].mean()
        print(f'Total de consultas realizadas: {len(df)}')
        print(f'Promedio de temperatura: {promedio:.2f} grados °C')

    def menu3(self):
       '''
        Metodo que genera el menu de consultas historicas (opcion 3 del menu principal).
        Permite al usuario consultar el historial de datos meteorologicos de una localidad dentro de un rango de fechas especificas.
        Llama a la API y procesa los datos y muestra resultados y graficos.
        '''
       while True:
        print(f"""{"-"*30}
Historicos:
0. Volver al menu anterior
1. Consulta por periodo de tiempo """)
        opcion3 = input('Seleccione una opcion: ')
        if opcion3 =='0':
            self.menu_p()
        elif opcion3 =='1':
            opcion4 = input('Escriba el nombre de la localidad: ').lower().strip()
            localidad_hallada = None
            for municipio in  self.lista_municipios:
                for loc in municipio.local:
                    if opcion4 in loc.local.lower() and loc.tiene_coordenadas():
                        localidad_hallada = loc
                        break
                if localidad_hallada:
                    break
            if localidad_hallada is None:
                print ('Localidad no encontrada')
            else:
                print(f'Localidad hallada: {localidad_hallada.local}')
                fecha_inicio = input('Ingrese fecha de inicio (AAAA-MM-DD): ')
                fecha_fin = input('Ingrese fecha de fin (AAAA-MM-DD): ')
                
                if not self.validar_fecha(fecha_fin) or not self.validar_fecha(fecha_fin):
                    print('Introduzca una fecha valida (AAAA-MM-DD)')
                    continue
                if fecha_inicio > fecha_fin:
                    print('La fecha de inicio debe ser anterior a la de fin')
                    continue
                
                df_datos = self.obtener_historicos_api(localidad_hallada.lat, localidad_hallada.long, fecha_inicio, fecha_fin)
                if df_datos is not None:
                    self.procesar_historicos(localidad_hallada.local, df_datos)        

        else:
            print('Opcion no valida')
            continue

    def validar_fecha(self,texto):
        '''
        Metodo que valida que el formato de las fechas sea correcto.
        Devuelve la fecha.
        '''
        partes = texto.split('-')
        if len(partes) !=3:
            return False
        anio = partes[0]
        mes = partes[1]
        dia = partes[2]
        if not (anio.isnumeric() and mes.isnumeric() and dia.isnumeric()):
            return False
        if len(anio) != 4:
            return False
        return 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31
    
    def obtener_historicos_api(self, lat, long, fecha_inicio, fecha_fin):
        '''
        Metodo que realiza la peticion de datos a la API.
        Recibe las coordenadas geograficas de la localidad y el rango de fechas.
        Devuelve el data frame de pandas renombras con nombres mas cortos para su procesamiento.
        Utiliza pandas.
        '''
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={fecha_inicio}&end_date={fecha_fin}&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max&timezone=America%2FNew_York"
        try:
             res = requests.get(url)
             datos = res.json()

             if 'daily' not in datos:
                 print('No se encontraron datos para esa fecha')
                 return None

             df = pd.DataFrame(datos['daily'])
             df['time'] = pd.to_datetime(df["time"])

            #renombrar las columnas para no usar los nombres largos que da la API

             df = df.rename(columns = {
            'temperature_2m_mean':'temperatura',
            'relative_humidity_2m_mean': 'humedad',
            'precipitation_sum':'precipitacion',
            'wind_speed_10m_max': 'viento'
             })

             return df 

        except Exception as e:
            print('Error en la fecha')
            return None

    def procesar_historicos(self,localidad_nombre, df):
        '''
        Metodo utilizado para procesar la data historica de la API.
        Calcula y muestra en consola las estadisticas agrupadas por mes, los promedios generales y un resumen de datos anual.
        Invoca el metodo para graficar.
        Utiliza pandas.
        '''
        df['anio']=df['time'].dt.year
        df['mes']=df['time'].dt.strftime('%Y-%m')
        
        print(f'''{'-'*30} Datos mensuales historicos: {localidad_nombre}''')
        meses_unicos = df['mes'].unique()

        for m in meses_unicos:
            df_mes = df[df['mes'] == m]
            print(f'''{'-'*30}Mes: {m}
Temperatura promedio: {df_mes['temperatura'].mean():.2f} grados °C
Humedad relativa promedio: {df_mes['humedad'].mean():.2f}%
Precipitacion acomulada: {df_mes['precipitacion'].sum():.2f} mm
Velocidad del viento promedio: {df_mes['viento'].mean():.2f} km/h ''')

        print(f'''Promedios generales del periodo
Temperatura media: {df['temperatura'].mean():.2f} grados °C
Humedad relativa media: {df['humedad'].mean():.2f}%
Precipitacion media diaria: {df['precipitacion'].mean():.2f} mm
Velocidad del viento media: {df['viento'].mean():.2f} km/h ''')

        anios_unicos = df['anio'].unique()

        max_temp, caluroso_anio = None, None
        min_temp, fresco_anio = None, None
        max_lluvia, lluvias_anio = None, None
        max_humedad, humedo_anio = None, None

        datos_anuales = {
            'anio':[],
            'temperatura':[],
            'humedad':[],
            'precipitacion':[],
            'viento':[]
        }
        for a in anios_unicos:
            df_a = df[df['anio'] == a]
            t_prom = df_a['temperatura'].mean()
            h_prom = df_a['humedad'].mean()
            p_total = df_a['precipitacion'].sum()
            v_prom = df_a['viento'].mean()

            datos_anuales['anio'].append(str(a))
            datos_anuales['temperatura'].append(t_prom)
            datos_anuales['humedad'].append(h_prom)
            datos_anuales['precipitacion'].append(p_total)
            datos_anuales['viento'].append(v_prom)

            if max_temp is None or t_prom > max_temp:
                max_temp = t_prom
                caluroso_anio = a

            if min_temp is None or t_prom < min_temp:
                min_temp = t_prom
                fresco_anio = a

            if max_lluvia is None or p_total > max_lluvia:
                max_lluvia = p_total
                lluvias_anio = a

            if max_humedad is None or h_prom > max_humedad:
                max_humedad = h_prom
                humedo_anio = a

        print(f'''{'-'*30} Resumen de anios:
Anio mas caluroso: {caluroso_anio} ({max_temp:.2f} °C) 
Anio mas fresco: {fresco_anio} ({min_temp:.2f} °C)  
Anio con mayor precipitacion acomulada: {lluvias_anio} ({max_lluvia:.2f} mm)
Anio mas humedo: {humedo_anio} ({max_humedad:.2f} %) ''' )

        df_anual = pd.DataFrame(datos_anuales)

        self.graficar_historicos(df_anual, localidad_nombre)

    def graficar_historicos(self, df_anual, localidad_nombre):
        '''
        Metodo que genera el grafico de los datos anuales de una localidad.
        Crea una figura con 4 subgraficos comparativos.
        Utiliza matplotlib.
        '''

        fig, axs = plt.subplots(4, 1, figsize = (9, 9), sharex = True)
        fig.suptitle(f'Evolucion anual- {localidad_nombre}', fontsize = 14)

        #Temperatura
        axs[0].plot(df_anual['anio'], df_anual['temperatura'], marker = '*', color = 'purple')
        axs[0].set_title('Temperatura media anual', fontsize=10)
        axs[0].set_ylabel('Temperatura (°C)')
        axs[0].grid(True)

        #Humedad
        axs[1].plot(df_anual['anio'], df_anual['humedad'], marker = '*', color = 'steelblue')
        axs[1].set_title('Humedad relativa media anual', fontsize=10)
        axs[1].set_ylabel('Humedad (%)')
        axs[1].grid(True)

        #Precipitacion
        axs[2].plot(df_anual['anio'], df_anual['precipitacion'], marker = '*', color = 'green')
        axs[2].set_title('Precipitacion acomulada anual', fontsize=10)
        axs[2].set_ylabel('Precipitacion total (mm)')
        axs[2].grid(True)

        #Velocidad del viento
        axs[3].plot(df_anual['anio'], df_anual['viento'], marker = '*', color = 'red')
        axs[3].set_title('Velocidad del viento media anual', fontsize=10)
        axs[3].set_ylabel('Velocidad del viento (km/h)')
        axs[3].set_xlabel('Anio')
        axs[3].grid(True)
        plt.setp(axs[3].get_xticklabels(), rotation=45)

        plt.tight_layout(rect = [0, 0, 1, 0.97])
        plt.show()