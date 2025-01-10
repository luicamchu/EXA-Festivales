from collections import Counter, defaultdict
import csv
from datetime import date, datetime, time
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
def lee_festivales(ruta:str) -> List[Festival]:
    res:List[Festival] = []
    with open(ruta, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for nombre, fecha_ini, fecha_fin, estado, precio, entradas, artistas, top in reader:
            nombre, estado, precio, entradas = nombre.strip(), estado.strip(), float(precio.replace(",", ".").strip()), int(entradas.strip())
            fecha_ini = parsea_fecha(fecha_ini)
            fecha_fin = parsea_fecha(fecha_fin)
            artistas = parsea_artistas(artistas)
            top = True if (top.strip().upper() == "SI" or top.strip().upper() == "SÍ") else False
            res.append(Festival(nombre, fecha_ini, fecha_fin, estado, precio, entradas, artistas, top))
    return sorted(res, key=lambda x:x.fecha_comienzo, reverse=False)

def parsea_fecha(fecha:str) -> date:
    return datetime.strptime(fecha, "%Y-%m-%d").date()
def parsea_hora(hora:str) -> time:
    return datetime.strptime(hora, "%H:%M").time()
def parsea_artistas(artistas:str) -> List[Artista]:
    res:List[Artista] = []
    lista_datos_artistas = artistas.split("-")
    for l in lista_datos_artistas:
        campos = l.split("_")
        if len(campos) == 3:
            nombre = campos[0].strip()
            hora_comienzo = parsea_hora(campos[1].strip())
            cache = int(campos[2].strip())
            res.append(Artista(nombre, hora_comienzo, cache))
    return res

def total_facturado(festivales:List[Festival], fecha_ini:Optional[date]=None, fecha_fin:Optional[date]=None)->float:
    if fecha_ini == None:
        fecha_ini = date.min
    if fecha_fin == None:
        fecha_fin = date.max
    total = sum(facturar(festival) for festival in festivales if festival.estado == "CELEBRADO" \
        and (fecha_ini <= festival.fecha_comienzo) and (festival.fecha_fin <= fecha_fin))
    return total

def facturar(festival:Festival) -> float:
    return festival.precio * festival.entradas_vendidas

def artista_top(festivales: List[Festival]) -> Tuple[int, str]:
    res = Counter(artista.nombre for festival in festivales for artista in festival.artistas if festival.estado == "CELEBRADO")
    top = max(res.items(), key=lambda x:x[1])
    return (top[1], top[0])

def artista_top2(festivales: List[Festival]) -> Tuple[int, str]:
    dicc = dict()
    for festival in festivales:
        for artista in festival.artistas:
            if festival.estado == "CELEBRADO":
                if artista.nombre not in dicc:
                    dicc[artista.nombre] = 1
                else:
                    dicc[artista.nombre] += 1
    top = max(dicc.items(), key=lambda x:x[1])
    return (top[1], top[0])

def mes_mayor_beneficio_medio(festivales: List[Festival]) -> str:
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", \
             "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    d:Dict[str, List[float]] = defaultdict(list)
    for festival in festivales:
        #d[meses[festival.fecha_comienzo.month-1]] = calcular_beneficio_por_festival(festival)
        d[meses[festival.fecha_comienzo.month-1]].append(calcular_beneficio_por_festival(festival))
    d_medias = {mes:sum(beneficio)/len(beneficio) for mes, beneficio in d.items()}

    return max(d_medias.items(), key=lambda x:x[1])[0]

def calcular_beneficio_por_festival(festival:Festival):
    cache_artistas = sum(artista.cache * 1000 for artista in festival.artistas)
    return (festival.precio * festival.entradas_vendidas) - cache_artistas

def artistas_comunes(festivales: List[Festival], festi1: str, festi2:str) -> List[str]:
    res:List[str] = []
    conjunto_artistas_f1 = set()
    conjunto_artistas_f2 = set()
    for festival in festivales:
        if festival.nombre == festi1:
             conjunto_artistas_f1 = {artista.nombre for artista in festival.artistas}
        if festival.nombre == festi2:
             conjunto_artistas_f2 = {artista.nombre for artista in festival.artistas}
    #return list(conjunto_artistas_f1.intersection(conjunto_artistas_f2))
    return list(conjunto_artistas_f1 & conjunto_artistas_f2)

def festivales_top_calidad_por_duracion(festivales: List[Festival], n: int=3) -> Dict[int, List[str]]:
    dicc = defaultdict(list)
    for festival in festivales:
        duracion = (festival.fecha_fin - festival.fecha_comienzo).days
        dicc[duracion].append(festival)
        #dicc[duracion] = festival
    return {duracion:festivales_top(lista_festivales, n) for duracion, lista_festivales in dicc.items()}

def festivales_top(lista_festivales, n):
    festivales_ordenados = sorted(lista_festivales, key=lambda x:calidad(x), reverse=True)[:n]
    return [festival.nombre for festival in festivales_ordenados]

def calidad(festival):
    return festival.entradas_vendidas/len(festival.artistas)