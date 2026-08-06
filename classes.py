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

class RegistroConsulta:
    '''
    Clase de registro y sus atributos. Utilizada en app.py para guardar los registros del usuario
    para poder ser usados en sus respectivos casos, especificamente en App.py menu1 y menu2.
    '''
    def __init__ (self, municipio, localidad, temperatura):
        self.municipio = municipio # str
        self.localidad = localidad #str
        self.temperatura = temperatura #float