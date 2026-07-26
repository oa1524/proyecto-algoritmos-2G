class Municipio:
    """
    Clase municipio con atributos.
    """
    def __init__(self, nombre, local):
        self.nombre = nombre # -> str
        self.local = local # -> lista

class Localidad:
    def __init__(self, local, lat, long):
        self.local = local # -> str
        self.lat = lat # -> float
        self.long = long # -> float