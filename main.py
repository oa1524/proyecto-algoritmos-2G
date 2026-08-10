# Grupo 2G: Omaira Alcala y Maria Algarra
# link al repositorio de GitHub: https://github.com/oa1524/proyecto-algoritmos-2G.git
from App import App

def main():
    '''
    Funcion main donde se crea un objeto de la clase App, se le aplica el metodo start que contiene 
    todas las funcionalidades de la aplicacion/programa.
    '''
    app = App()
    app.start()

'''
Llamado a la funcion main para poder iniciar el programa cuando la condicion de if se cumpla,
es decir, siempre.
'''
if __name__ == '__main__':
    main()