from f import *

def test_lee_festivales(festivales:List[Festival]) -> None:
    print("Test lee_festivales")
    print(f"Total festivales: {len(festivales)}")
    print("Los tres primeros:")
    for f in festivales[:3]:
        print(f)
        print("\n")


if __name__=="__main__":
    print("Test Ej1: lee_festivales")
    festivales = lee_festivales("data\\festivales.csv")
    test_lee_festivales(festivales) 
    print("\n")
    print("Test Ej2: total_facturado")
    print(f"Total facturado: {total_facturado(festivales, None, None)}")
    print("\n")
    print("Test Ej3: artista_top")
    print(f"Artista Top: {artista_top(festivales)}")
    print("\n")
    print("Test Ej4: mes_mayor_beneficio_medio")
    print(f"Mes Mayor Beneficio: {mes_mayor_beneficio_medio(festivales)}")
    print("\n")
    print("Test Ej5: artistas_comunes")
    print(f"Lista de Artistas en festivales comunes: {artistas_comunes(festivales, "Creamfields", "Tomorrowland")}")
    print("Test Ej6: festivales_top_calidad_por_duracion")
    print(f"Festibales top por calidad: {festivales_top_calidad_por_duracion(festivales, 3)}")
    print("\n")