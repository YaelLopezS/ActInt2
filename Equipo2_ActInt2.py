"""-------------- ACTIVIDAD INTEGRADORA 2 --------------"""


"""-------------- EQUIPO 2 --------------"""
# Irving Yael López Solis - A01664809
# Diego Alejandro Anaya Alanis - A01663765
# Fernando Manuel Chiñas Salinas - A00832747


import sys
from collections import deque, defaultdict

def leer_datos_desde_archivo(nombre_archivo):
    """
    Lee los datos de un archivo y los organiza en el formato necesario.
    
    Args:
        nombre_archivo (str): El nombre del archivo que contiene los datos.

    Returns:
        tuple: Número de colonias, matriz de distancias y matriz de capacidades.
    """
    with open(nombre_archivo, 'r') as archivo:
        # Leer el número de colonias
        num_colonias = int(archivo.readline().strip())
        
        # Leer la matriz de distancias
        grafo_distancias = []
        for _ in range(num_colonias):
            fila = list(map(int, archivo.readline().strip().split()))
            grafo_distancias.append(fila)
        
        # Leer la matriz de capacidades
        grafo_capacidades = []
        for _ in range(num_colonias):
            fila = list(map(int, archivo.readline().strip().split()))
            grafo_capacidades.append(fila)
        
    return num_colonias, grafo_distancias, grafo_capacidades

def prim_mst(num_colonias, grafo):
    """
    Calcula el Árbol de Expansión Mínima (MST) de un grafo ponderado no dirigido utilizando el 
    algoritmo de Prim. El MST conecta todas las colonias con la mínima longitud de cableado 
    necesario, optimizando el costo.

    Args:
        num_colonias (int): Número de colonias o nodos en el grafo.
        grafo (list[list[int]]): Matriz de adyacencia que representa el grafo con las distancias
                                  en kilómetros entre las colonias.

    Returns:
        list[tuple[int, int]]: Lista de aristas en el MST, donde cada arista se representa como 
                               una tupla (A, B) que indica una conexión entre las colonias A y B.
    """
    en_mst = [False] * num_colonias  # Rastrea qué nodos ya están en el MST
    arista_minima = [(float('inf'), -1)] * num_colonias  # Inicializa las aristas mínimas con infinito
    arista_minima[0] = (0, -1)  # Comienza desde el nodo 0
    aristas_mst = []  # Lista para almacenar las aristas del MST

    for _ in range(num_colonias):
        # Encuentra el nodo no incluido en el MST con la arista de peso mínimo
        u = min((peso, v) for v, (peso, _) in enumerate(arista_minima) if not en_mst[v])[1]
        en_mst[u] = True  # Marca el nodo como incluido en el MST
        
        if arista_minima[u][1] != -1:
            # Agrega la arista al MST
            aristas_mst.append((arista_minima[u][1], u))

        # Actualiza las aristas mínimas para los vecinos del nodo u
        for v, peso in enumerate(grafo[u]):
            if not en_mst[v] and peso < arista_minima[v][0] and peso > 0:
                arista_minima[v] = (peso, u)  # Actualiza la arista mínima para el vecino

    return aristas_mst

def bfs_encontrar_camino(capacidad, flujo, fuente, flow):
    """
    Realiza una búsqueda en anchura (BFS) para encontrar un camino de aumento en el grafo residual.

    Args:
        capacidad (list[list[int]]): Matriz que representa la capacidad máxima de flujo entre
                                     cada par de nodos.
        flujo (list[list[int]]): Matriz que representa el flujo actual en cada arista entre
                                 nodos en el grafo.
        fuente (int): Nodo de inicio en la búsqueda del camino de aumento.
        flow (int): Nodo destino en la búsqueda del camino de aumento.

    Returns:
        tuple[int, list[int]]: Flujo de aumento encontrado en el camino y la lista de nodos padres.
    """
    padre = [-1] * len(capacidad)  # Rastrea el camino
    padre[fuente] = -2  # Marcamos la fuente como el nodo de inicio
    cola = deque([(fuente, float('inf'))])  # Cola para BFS

    while cola:
        u, flujo_camino = cola.popleft()  # Nodo actual y flujo disponible

        for v in range(len(capacidad)):
            # Si no hemos visitado el nodo y hay capacidad disponible
            if padre[v] == -1 and capacidad[u][v] - flujo[u][v] > 0:
                padre[v] = u  # Guardamos el nodo padre
                nuevo_flujo = min(flujo_camino, capacidad[u][v] - flujo[u][v])
                if v == flow:
                    return nuevo_flujo, padre  # Si llegamos al destino, retornamos el flujo encontrado
                cola.append((v, nuevo_flujo))  # Agregamos el vecino a la cola

    return 0, padre

def edmonds_karp_flujo_maximo(num_nodos, capacidad, fuente, flow):
    """
    Calcula el flujo máximo en un grafo desde el nodo fuente hasta el nodo destino usando 
    el algoritmo de Edmonds-Karp.

    Args:
        num_nodos (int): Número de nodos en el grafo.
        capacidad (list[list[int]]): Matriz de capacidad máxima de flujo entre cada par de nodos.
        fuente (int): Nodo de inicio para calcular el flujo máximo.
        flow (int): Nodo final para calcular el flujo máximo.

    Returns:
        int: El flujo máximo posible desde el nodo fuente al destino.
    """
    flujo = [[0] * num_nodos for _ in range(num_nodos)]  # Matriz de flujo inicializada a 0
    flujo_maximo = 0  # Inicializamos el flujo máximo a 0

    while True:
        flujo_camino, padre = bfs_encontrar_camino(capacidad, flujo, fuente, flow)  # Encuentra un camino de aumento
        if flujo_camino == 0:  # Si no hay más caminos de aumento, termina
            break
        flujo_maximo += flujo_camino  # Aumentamos el flujo máximo
        v = flow

        # Actualizamos los flujos a lo largo del camino encontrado
        while v != fuente:
            u = padre[v]
            flujo[u][v] += flujo_camino  # Aumentamos el flujo en la dirección hacia adelante
            flujo[v][u] -= flujo_camino  # Disminuimos el flujo en la dirección opuesta
            v = u

    return flujo_maximo

def ruta_para_personal(grafo, inicio=0):
    """
    Encuentra una ruta aproximada para el problema del Viajero usando el método de vecino más cercano.
    
    Args:
        grafo (list[list[int]]): Matriz de adyacencia que representa las distancias entre colonias.
        inicio (int): Nodo inicial (colonia de inicio) de la ruta.

    Returns:
        tuple[list[int], int]: Retorna la ruta calculada y la distancia total de la ruta.
    """
    num_nodos = len(grafo)
    visitado = [False] * num_nodos  # Lista para rastrear qué colonias se han visitado
    ruta = [inicio]  # Comenzamos en la colonia de inicio
    distancia_total = 0  # Distancia total del recorrido
    actual = inicio
    visitado[actual] = True  # Marcamos la colonia de inicio como visitada

    for _ in range(num_nodos - 1):
        siguiente, distancia_minima = -1, float('inf')
        # Busca el vecino más cercano que aún no haya sido visitado
        for vecino in range(num_nodos):
            # Si el vecino no ha sido visitado, es accesible (peso > 0), y tiene la menor distancia encontrada
            if not visitado[vecino] and grafo[actual][vecino] > 0 and grafo[actual][vecino] < distancia_minima:
                siguiente, distancia_minima = vecino, grafo[actual][vecino]

        ruta.append(siguiente)  # Añade el vecino más cercano a la ruta
        distancia_total += distancia_minima  # Actualiza la distancia total
        visitado[siguiente] = True  # Marca el vecino como visitado
        actual = siguiente  # Actualiza el nodo actual

    ruta.append(inicio)  # Vuelve al nodo de inicio para cerrar el ciclo
    distancia_total += grafo[actual][inicio]  # Añade la distancia de vuelta al inicio

    return ruta, distancia_total

def main():
    # Leer los datos del archivo
    num_colonias, grafo_distancias, grafo_capacidades = leer_datos_desde_archivo('datos.txt')
    
    # Calculamos el Árbol de Expansión Mínima (MST)
    aristas_mst = prim_mst(num_colonias, grafo_distancias)
    mst_str = ", ".join(f"({u}, {v})" for u, v in aristas_mst)
    print(mst_str)  # Imprimir la forma de cablear las colonias con fibra óptica

    # Calculamos la ruta para el personal (usando TSP aproximado)
    ruta, distancia_total = ruta_para_personal(grafo_distancias)
    ruta_str = ", ".join(f"({ruta[i]}, {ruta[i+1]})" for i in range(len(ruta) - 1))
    print(ruta_str)  # Imprimir la ruta para el personal

    # Calculamos el flujo máximo de información
    flujo_maximo = edmonds_karp_flujo_maximo(num_colonias, grafo_capacidades, 0, num_colonias - 1)
    print(f"{flujo_maximo}")  # Imprimir el valor del flujo máximo de información

if __name__ == "__main__":
    main()
