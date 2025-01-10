from festivales import lee_festivales


from festivales import *

def test_lee_festivales (festivales:List[Festival])->None:
    print("Test lee_festivales")
    print(f"Total festivales: {len(festivales)}")
    print("Los tres primeros:")
    print(festivales[:2])

def test_total_facturado(festivales:List[Festival], fecha_ini:Optional[date]=None, fecha_fin:Optional[date]=None)->None:
    res = total_facturado(festivales, fecha_ini, fecha_fin)
    print(f"Entre {fecha_ini} y {fecha_fin} el total es: {res}")

def test_artista_top(festivales: List[Festival]) -> None:
    num_festivales, artista = artista_top(festivales)
    print(f"El artista que ha actuado en más festivales es {artista}, con {num_festivales} festivales.")

def test_mes_mayor_beneficio_medio(festivales: List[Festival]) -> None:
    res = mes_mayor_beneficio_medio(festivales)
    print(f"El mes con más beneficio medio es {res}")
    
def test_artistas_comunes(festivales: List[Festival], festi1: str, festi2:str) -> None:
    res = artistas_comunes(festivales, festi1, festi2)
    print(f"Los artistas comunes entre {festi1} y {festi2} son {res}")

def test_festivales_top_calidad_por_duracion(festivales: List[Festival], n: int=3)->None:
    res = festivales_top_calidad_por_duracion(festivales, n)
    print(f"Los mejores {n} festivales por número de días son:")
    for duracion, festivales in res.items():
        print(f"{duracion} : {festivales}")

if __name__=="__main__":
    festivales = lee_festivales("data\\festivales.csv")
    test_lee_festivales(festivales) 
    
    print("Test Ej2: total_facturado")
    test_total_facturado(festivales, None, None)
    test_total_facturado(festivales, fecha_fin=date(2024,6,15))
    test_total_facturado(festivales, fecha_ini=date(2024,6,15))
    test_total_facturado(festivales, date(2024,6,1), date(2024,6,15))
    test_total_facturado(festivales, date(2024,6,1), date(2024,6,23))
    
    
    print("Test Ej3: artista_top")
    test_artista_top(festivales)

    print("Test Ej4: mes_mayor_beneficio_medio")
    test_mes_mayor_beneficio_medio(festivales)

    print("Test 5: artistas_comunes")
    test_artistas_comunes(festivales,"Creamfields", "Tomorrowland")
    test_artistas_comunes(festivales,"Primavera Sound", "Coachella")
    test_artistas_comunes(festivales,"Iconica Fest", "Primavera Sound")

    print("Test 6: festivales_top_mejor_ratio")
    test_festivales_top_calidad_por_duracion(festivales, 1)
    test_festivales_top_calidad_por_duracion(festivales, 3)
    