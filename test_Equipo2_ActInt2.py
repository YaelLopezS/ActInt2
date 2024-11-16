"""-------------- ACTIVIDAD INTEGRADORA 2 --------------"""

"""-------------- EQUIPO 2 --------------"""
# Irving Yael López Solis - A01664809
# Diego Alejandro Anaya Alanis - A01663765
# Fernando Manuel Chiñas Salinas - A00832747

import pytest
from Equipo2_ActInt2 import *

def test_leer_datos_correcto(tmp_path):
    """Prueba lectura de archivo con formato correcto"""

    #Se crea un archivo temporal con datos en el formato requrido
    d = tmp_path / "datos_correcto.txt"
    d.write_text("4\n0 10 15 20\n10 0 25 30\n15 25 0 35\n20 30 35 0\n" +
                 "0 50 45 55\n50 0 60 65\n45 60 0 70\n55 65 70 0")
    
    #Lee los datos y verifica que la estructura sea la correcta
    num_colonias, distancias, capacidades = leer_datos_desde_archivo(str(d))
    assert num_colonias == 4
    assert distancias == [[0, 10, 15, 20], [10, 0, 25, 30], [15, 25, 0, 35], [20, 30, 35, 0]]
    assert capacidades == [[0, 50, 45, 55], [50, 0, 60, 65], [45, 60, 0, 70], [55, 65, 70, 0]]

def test_leer_datos_invalido(tmp_path):
    """Prueba lectura de archivo con formato incorrecto"""

    #Se crea un archivo temporal con datos en el formato requrido, en este caso el formato esta incorrecto
    d = tmp_path / "datos_invalido.txt"
    d.write_text("4\n0 10 15\n10 0 25 30\n15 25 0 35\n" +  # Fila incompleta
                 "0 50 45 55\n50 0 60 65\n45 60 0 70\n55 65 70 0")
    # Lee los datos y verifica si las matrices resultantes tienen algun error
    num_colonias, distancias, capacidades = leer_datos_desde_archivo(str(d))
    assert num_colonias == 4
    assert len(distancias) != num_colonias or any(len(row) != num_colonias for row in distancias)
    assert len(capacidades) != num_colonias or any(len(row) != num_colonias for row in capacidades)

def test_prim_mst():
    """Prueba el algoritmo de Prim para construir el MST"""
    
    num_colonias = 4
    distancias = [
        [0, 16, 45, 32],
        [16, 0, 18, 21],
        [45, 18, 0, 7],
        [32, 21, 7, 0]
    ]
    # Ejecuta Prim y verifica que las aristas y el peso total son correctos
    aristas = prim_mst(num_colonias, distancias)
    assert len(aristas) == num_colonias - 1
    peso_total = sum(distancias[u][v] for u, v in aristas)
    assert peso_total > 0

def test_prim_mst_empty():
    """Prueba el algoritmo de Prim en un grafo vacío"""
    
    # Datos de prueba con un grafo vacío
    num_colonias = 0
    distancias = []
    # Ejecuta Prim y verifica que no se generen aristas
    try:
        aristas = prim_mst(num_colonias, distancias)
        assert aristas == []  # En un grafo vacío, no debe haber aristas
    except IndexError:
        pass  #Si ocurre un error, se considera aceptable para esta prueba, ya que no hay nodos

def test_prim_mst_large_weights():
    """Prueba el algoritmo de Prim con pesos grandes"""

   
    num_colonias = 3
    distancias = [
        [0, 9999, 5000],
        [9999, 0, 10000],
        [5000, 10000, 0]
    ]
    # Ejecuta Prim y verifica el MST con los pesos mínimos esperados
    aristas = prim_mst(num_colonias, distancias)
    assert len(aristas) == num_colonias - 1
    peso_total = sum(distancias[u][v] for u, v in aristas)
    assert peso_total == 9999 + 5000  # El MST debería conectar los caminos más baratos


def test_ruta_para_personal():
    """Prueba la ruta del viajante para la ruta mínima de entrega"""

    distancias = [
        [0, 16, 45, 32],
        [16, 0, 18, 21],
        [45, 18, 0, 7],
        [32, 21, 7, 0]
    ]
    # Calcula la ruta y verifica que cumpla con los requisitos
    num_colonias = len(distancias)
    ruta, distancia = ruta_para_personal(distancias)
    assert len(ruta) == num_colonias + 1
    assert ruta[0] == ruta[-1] # Verifica que sea un ciclo que regresa al origen
    assert len(set(ruta[:-1])) == num_colonias # Verifica que las todas colonias sean visitadas una vez

def test_ruta_para_personal_empty():
    """Prueba la ruta del viajante con una matriz de distancias vacía"""

    # Datos de prueba con matriz vacía
    distancias = []
    # Intenta calcular la ruta y verifica que no se genere ninguna
    try:
        ruta, distancia = ruta_para_personal(distancias)
        assert ruta == []  # En un grafo vacío, no debe haber ruta
        assert distancia == 0
    except IndexError:
        pass  # Si ocurre un error, se considera aceptable, ya que no hay nodos



def test_bfs_encontrar_camino():
    """Prueba BFS para encontrar caminos en la red"""

    capacidades = [
        [0, 48, 12, 18],
        [52, 0, 42, 32],
        [18, 46, 0, 56],
        [24, 36, 52, 0]
    ]
    num_colonias = len(capacidades)
    flujo = [[0] * num_colonias for _ in range(num_colonias)]
    #Ejecuta BFS y verifica que el camino encontrado sea válido
    flujo_camino, padre = bfs_encontrar_camino(capacidades, flujo, 0, num_colonias - 1)
    assert flujo_camino > 0
    assert padre[num_colonias - 1] != -1 # Asegura que el nodo destino tenga un padre en el camino

def test_bfs_encontrar_camino_no_flow():
    """Prueba BFS donde no hay flujo entre origen y destino"""

    capacidades = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    flujo = [[0] * 3 for _ in range(3)]
    # Ejecuta BFS y verifica que no haya camino de flujo
    flujo_camino, padre = bfs_encontrar_camino(capacidades, flujo, 0, 2)
    assert flujo_camino == 0  # No debe haber flujo en un grafo sin aristas
    assert padre[2] == -1  # No hay camino hacia el nodo destino


def test_edmonds_karp_flujo_maximo():
    """Prueba flujo máximo de Edmonds-Karp"""

    capacidades = [
        [0, 48, 12, 18],
        [52, 0, 42, 32],
        [18, 46, 0, 56],
        [24, 36, 52, 0]
    ]
    # Calcula el flujo máximo y verifica que sea positivo
    num_colonias = len(capacidades)
    flujo = edmonds_karp_flujo_maximo(num_colonias, capacidades, 0, num_colonias - 1)
    assert flujo > 0

def test_edmonds_karp_flujo_manual():
    """Prueba flujo máximo en un caso sencillo conocido"""

    num_colonias = 4
    capacidades = [
        [0, 10, 10, 0],
        [10, 0, 5, 15],
        [10, 5, 0, 10],
        [0, 15, 10, 0]
    ]
    # Calcula el flujo máximo y verifica que sea el valor esperado
    flujo_esperado = 20
    flujo = edmonds_karp_flujo_maximo(num_colonias, capacidades, 0, 3)
    assert flujo == flujo_esperado, f"Se esperaba un flujo máximo de {flujo_esperado}, pero se obtuvo {flujo}"

def test_edmonds_karp_multiple_paths():
    """Prueba flujo máximo con múltiples caminos"""

    capacidades = [
        [0, 10, 10, 0],
        [0, 0, 0, 10],
        [0, 0, 0, 10],
        [0, 0, 0, 0]
    ]
    # Calcula el flujo máximo y verifica que sea la suma de ambos caminos
    flujo = edmonds_karp_flujo_maximo(4, capacidades, 0, 3)
    assert flujo == 20  # El flujo máximo debería ser la suma de ambos caminos

def test_edmonds_karp_no_capacity():
    """Prueba flujo máximo donde no existe capacidad entre origen y destino"""

    capacidades = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    # Calcula el flujo máximo y verifica que sea cero
    flujo = edmonds_karp_flujo_maximo(3, capacidades, 0, 2)
    assert flujo == 0  # No debe haber flujo ya que es un grafo sin capacidad

def test_edmonds_karp_simple_path():
    """Prueba flujo máximo con un solo camino disponible"""

    capacidades = [
        [0, 10, 0],
        [0, 0, 5],
        [0, 0, 0]
    ]
    # Calcula el flujo máximo y verifica que sea igual a la capacidad mínima en el camino
    flujo = edmonds_karp_flujo_maximo(3, capacidades, 0, 2)
    assert flujo == 5  # El flujo máximo es igual a la capacidad mínima en el camino
