from collections import defaultdict, Counter
import statistics
from typing import NamedTuple, List, Dict, Tuple, Optional
import csv
from datetime import date, datetime, time

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
                        ("top", bool)])

##########################################################################################
# EJERCICIO 1
##########################################################################################
def lee_festivales (archivo:str) -> List[Festival]:
    res=[]
    with open(archivo, mode= 'r', encoding= "utf-8") as f:
        
        lector = csv.reader(f, delimiter=',')
        next(lector)
        
        for nombre, fecha_ini, fecha_fin, estado, precio, entradas, artistas, top in lector:
        
            #pp :Duration = None
            fecha_ini = parsea_fecha(fecha_ini)
            fecha_fin = parsea_fecha (fecha_fin)
            precio    = float(precio.strip())
            entradas  = int(entradas.strip())
            artistas  = parsea_artistas(artistas.strip())
            top       = parsea_top(top.strip())
            
            res.append(Festival(nombre.strip(),
                                fecha_ini,
                                fecha_fin,
                                estado.strip().upper(),
                                precio,
                                entradas,
                                artistas,
                                top))
            
    # Se devuelve ordenada por fecha comienzo
    return sorted(res, key=lambda f: f.fecha_comienzo)   

def parsea_fecha(fecha_str: str) -> date:
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()

def parsea_artistas(artistas_str:str)->List[Artista]:
    
    res :list = []
    trozos = artistas_str.split("-")
    if trozos:
        res = [parsea_artista(trozo) for trozo in trozos]
    
    return res
    
def parsea_artista(artista_str:str)->Artista:
    
    res :Artista = None
    trozos = artista_str.split("_")
    if len(trozos) == 3:
        nombre = trozos[0].strip()
        hora   = parsea_hora(trozos[1].strip())
        cache  = int(trozos[2].strip())
        res    = Artista(nombre, hora, cache)
    
    return res

def parsea_hora(hora_str:str)->time:
    return datetime.strptime(hora_str, "%H:%M").time()

def parsea_top(top_str:str)->bool:
    
    res :bool = None
    
    if top_str.lower() == 'sí' or top_str.lower() == 'si':
        res = True
    elif (top_str.lower() == "no"):
        res = False
    
    return res

##########################################################################################
# EJERCICIO 2
# Función que devuelva el importe total facturado de los festivales que se han celebrado 
# entre dos fechas dadas. La función recibe una lista de tuplas de tipo `Festival` y dos 
# fechas, cuyos valores por defecto son `None`. La función devuelve un número real con el 
# total facturado por los festivales celebrados entre las dos fechas dadas. Si la fecha 
# inicial es `None` se hace el cálculo sin limitar la fecha mínima de los festivales. 
# Si la fecha final es `None` se hace el cálculo sin limitar la fecha máxima de los 
# festivales. Para calcular el total facturado por festival hay que multiplicar el número 
# de entradas por el precio de la entrada del festival. **Nota**: tenga en cuenta que la 
# función debe tomar la facturación de los festivales con estado _celebrado_ en el rango 
# de fechas, es decir, solo se tendrán en cuenta aquellos festivales que empiezan y acaban 
# dentro del rango de fechas.  
##########################################################################################
def total_facturado(festivales:List[Festival], 
                    fecha_ini:Optional[date] = None, 
                    fecha_fin:Optional[date] = None)->float:
 
    res :float = sum (facturacion(festival) for festival in festivales 
                                            if festival.estado == "CELEBRADO" and   
                                               en_fecha(festival, fecha_ini, fecha_fin))
    return res

def facturacion (festival: Festival)->float:
    return festival.entradas_vendidas * festival.precio

def en_fecha (festival: Festival, 
              fecha_ini:Optional[date] = None, 
              fecha_fin:Optional[date] = None)->bool:
    
    return (fecha_ini == None or fecha_ini <= festival.fecha_comienzo) and \
                                (fecha_fin == None or festival.fecha_fin <= fecha_fin)

##########################################################################################
# EJERCICIO 3
# Función que recibe una lista de tuplas de tipo `Festival` y devuelve una tupla compuesta 
# por un número entero y una cadena de texto, que representan el número de festivales y el 
# nombre del artista que haya participado en más festivales que finalmente se han celebrado, 
# respectivamente.
##########################################################################################
def artista_top(festivales: List[Festival]) -> Tuple[int, str]:

    c :Counter = contar_festivales_por_artista (festivales)  

    m = max(c.items(), key=lambda x:x[1] )
    return (m[1], m[0])

    # return max(dic.items(), key=lambda x: x[1])[::-1] # También se puede poner de forma más pythonica
			
def contar_festivales_por_artista(festivales:List[Festival]) -> Counter:
    
    res = Counter(artista.nombre for festival in festivales for artista in festival.artistas
                                                            if festival.estado == 'CELEBRADO')
    return res

def contar_festivales_por_artista2(festivales:List[Festival]) -> Dict[str, int]:
    res = defaultdict(int)
    
    for f in festivales:
        if f.estado == 'CELEBRADO':
            for a in f.artistas:
                res[a.nombre] += 1
    
    return res

##########################################################################################
# EJERCICIO 4
# recibe una lista de tuplas de tipo `Festival` y devuelve una cadena de texto que será 
# el nombre del mes, en español, de aquel que haya obtenido un mayor beneficio medio. 
# Es decir, cada festival tiene un beneficio que se calcula a partir de las entradas 
# vendidas menos el caché de los artistas. Pues esta función debe calcular el beneficio 
# medio que se ha obtenido cada mes y devolver aquel cuyo beneficio haya sido el mayor. 
# Nota: Si hubiera algún festival que se celebra entre dos meses, se imputará al mes en 
# el que comienza. Por ejemplo, un festival que comience el 30 de junio y acabe el 4 de 
# julio será imputado al mes de junio.
##########################################################################################

def mes_mayor_beneficio_medio(festivales: List[Festival]) -> str:
    
    d :Dict[str, List[float]] = beneficios_festivales_por_mes(festivales)
    d_medias = {mes:statistics.mean(beneficios) for mes, beneficios in d.items()}
    
    # Otra forma de hacerlo
    # d_medias = {mes:sum(beneficios)/len(beneficios) for mes, beneficios in d.items()}

    # res = max(d_medias.keys(), key=d_medias.get)     
    # return res

    # Otra forma de hacerlo
    res = max(d_medias.items(), key=lambda it:it[1])
    res = res[0] 
    return res
 
def beneficios_festivales_por_mes(festivales:List[Festival]) -> Dict[str, List[float]]:

    d = defaultdict(list)
    for festival in festivales:
        mes = mes_str(festival.fecha_comienzo)
        d[mes].append( calcula_beneficio(festival))
    return d

def mes_str(fecha:date)->str:
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", \
             "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[fecha.month - 1]
 
def calcula_beneficio (festival: Festival) ->float:
    cache_total = sum(artista.cache * 1000 for artista in festival.artistas)
    res = festival.entradas_vendidas * festival.precio - cache_total
    return res

##########################################################################################
# EJERCICIO 5
# Función que recibe una lista de tuplas de tipo `Festival` y dos cadenas de texto `festi1` 
# y `festi2`, y devuelve una lista con los nombres de aquellos artistas que se repitan 
# entre `festi1` y `festi2`  
##########################################################################################
def artistas_comunes(festivales: List[Festival], festi1: str, festi2:str) -> List[str]:
    
    a1 = a2 = set()
    for f in festivales:
        if f.nombre == festi1:
            a1 = {a.nombre for a in f.artistas}
        if f.nombre == festi2:
            a2 = {a.nombre for a in f.artistas}
    
    return list(a1.intersection(a2))

##########################################################################################
# EJERCICIO 6
# Cada festival tiene una duración de entre 2 y 8 días. Implemente una función que, 
# recibiendo una lista de tuplas de tipo `Festival`, y un número `n` cuyo valor por 
# defecto será 3, devuelva un diccionario en el que las claves son las duraciones de 
# los festivales, y los valores listas con los nombres de los `n` festivales de más 
# calidad (ordenados de más a menos calidad). La calidad de un festival viene dada 
# por el ratio entre entradas vendidas y número de artistas participantes en el festival. 
# Cuanto más alto es este ratio, más calidad tiene el festival.
##########################################################################################

def festivales_top_calidad_por_duracion(festivales: List[Festival], n: Optional[int]=3)->Dict[int, List[str]]:
    d   = festivales_por_duracion (festivales)
    res = { duracion: festivales_top_calidad(lista_festivales, n) for duracion, lista_festivales in d.items()}
    return res

def festivales_por_duracion(festivales: List[Festival])->Dict[int, List[Festival]]:
    res = defaultdict(list)
    for fest in festivales:
        duracion = (fest.fecha_fin-fest.fecha_comienzo).days
        res[duracion].append(fest)
    
    return res

def festivales_top_calidad(festivales: List[Festival], n: int=3)->List[str]:
    
    festivales_ord = sorted(festivales, key=lambda festival:calidad(festival), reverse=True)[:n]
    
    return[festival.nombre for festival in festivales_ord]

def calidad(festival:Festival)->float:
    
    return festival.entradas_vendidas/len(festival.artistas)