import json

def read():
    with open("zonas_caracas.json", "r", encoding="utf-8") as z:
        zonas = json.load(z)
        print(zonas)

    