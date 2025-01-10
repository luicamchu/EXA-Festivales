import csv
from typing import NamedTuple, List, Dict, Tuple, Optional, Set
 
Artista = NamedTuple("Artista",     
                        [("nombre", str), 
                        ("hora_comienzo", time), 
                        ("cache", int)])

Festival = NamedTuple("Festival", 
                        [("nombre", str),
                        ("fecha_comienzo", date),
                        ("fecha_fin", date),
                        ("estado", str),                      
                        ("precio", float),
                        ("entradas_vendidas", int),
                        ("artistas", List[Artista]),
                        ("top", bool)
                    ])


def lee_festivales (archivo:str)->List[Festival]:
    result:list[Festival] = []
    with open(archivo, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for denominacion, tipo, dificultad, ingredientes, tiempo, calorias, fecha, precio in reader:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            precio = float(precio.replace(",","."))
            calorias = int(calorias)
            lista_ingredientes = []                
            aux1= parseo(ingredientes, ",")
            for a in aux1:
                aux2 = parseo(a, "-")
                if len(aux2) == 3:
                    i = Ingrediente(aux2[0], aux2[1], aux2[2])
                    lista_ingredientes.append(i)
            r = Receta(denominacion, tipo, dificultad, lista_ingredientes, tiempo, calorias, fecha, precio)
            result.append(r)
    return result

def total_facturado(festivales:List[Festival], fecha_ini:Optional[date]=None, fecha_fin:Optional[date]=None)->float:
    pass

def artista_top(festivales: List[Festival]) -> Tuple[int, str]:
    pass

def mes_mayor_beneficio_medio(festivales: List[Festival]) -> str:
    pass