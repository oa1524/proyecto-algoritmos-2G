class Municipio:
    """
    Clase municipio con atributos.
    """
    def __init__(self, nombre, local):
        self.nombre = nombre # -> str
        self.local = local # -> lista

class Localidad:
    '''
    Clase localidad con atributos.
    '''
    def __init__(self, local, lat, long):
        self.local = local # -> str
        self.lat = lat # -> float
        self.long = long # -> float

    '''
    Funcion que indica si la localidad tiene coordenas registradas.
    '''
    def tiene_coordenadas(self):
        return self.lat is not None and self.long is not None


class RegistroConsulta:
    '''
    Clase de registro y sus atributos. Utilizada en app.py para guardar los registros del usuario
    para poder ser usados en sus respectivos casos, especificamente en App.py menu1 y menu2.
    '''
    def __init__ (self, municipio, localidad, temperatura):
        self.municipio = municipio #objeto Municipio
        self.localidad = localidad #objeto Localidad
        self.temperatura = temperatura #float

class ClimaActual:
    '''
    Clase clima para registrar la informacion de la API.
    '''
    def __init__(self, temperatura, humedad, viento, codigo_clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima

class Historico:
    '''
    Clase para registrar la informacion de historicos de la API.
    '''
    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento 