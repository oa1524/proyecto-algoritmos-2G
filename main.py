import read_json
import verificar_coord

def main():
    lista_municipios = read_json.read()
    print(lista_municipios)
    verificar_coord.ver_coord(lista_municipios)

if __name__ == '__main__':
    main()