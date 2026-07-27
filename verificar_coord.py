def ver_coord(list_municipios):
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