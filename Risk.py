"""
Este script, contiene el codigo que simula el juego del Risk.
Genero todas las posibles combinaciones de tropas (las que se observan definidas en parametros iniciales) respetando la puntuación máxima establecida de 20 puntos.
Genero todas las permutaciones posibles del orden a la hora de atacar a los territorios enemigos, respetando la regla que establece que debe haber al menos una
unidad de cada tropa (al menos una de infanería una de caballería y una de artillería) .
Al ejecutar el código, está la opción de datos personalizados, dejando al usuario cambiar parametros como: puntos disponibles, fuerza de cada tropa, número de
territorios enemigos y datos de cada territorio elegido (elegir la fuerza de defensa (int) y el tipo de terreno (str))
Prueba a usar los siguientes datos:
Puntos disponibles: 20
Fuerzas de las tropas:
Infantería: 1
Caballería: 3
Artillería: 5
Número de territorios enemigos: 3
Datos de los territorios:
Territorio 1: Defensa = 5, Tipo = plano
Territorio 2: Defensa = 6, Tipo = montaña
Territorio 3: Defensa = 4, Tipo = fortaleza
"""
from itertools import product, permutations

# Parámetros iniciales
infanteria_costo, caballeria_costo, artilleria_costo = 1, 3, 5
fuerza_tropas = {'infanteria': 1, 'caballeria': 3, 'artilleria': 5}
max_puntos = 20

# Generar combinaciones de tropas
def generar_combinaciones_tropas(max_puntos):
    combinaciones_validas = []
    for infanteria in range(max_puntos + 1):
        for caballeria in range((max_puntos // caballeria_costo) + 1):
            for artilleria in range((max_puntos // artilleria_costo) + 1):
                costo_total = (infanteria * infanteria_costo +
                               caballeria * caballeria_costo +
                               artilleria * artilleria_costo)
                # Verificar costo y presencia de al menos una unidad de cada tropa
                if costo_total <= max_puntos and infanteria > 0 and caballeria > 0 and artilleria > 0:
                    combinaciones_validas.append((infanteria, caballeria, artilleria))
    return combinaciones_validas

# Generar permutaciones del orden de ataque
def generar_permutaciones_ataques(territorios, regla_debil=False, tablero=None):
    if regla_debil and tablero:
        territorios_ordenados = sorted(territorios, key=lambda x: tablero[x]['defensa'])
        return list(permutations(territorios_ordenados))
    return list(permutations(territorios))

# Evaluar si una combinación de tropas puede conquistar los territorios en un orden dado
def evaluar_combinacion(combinacion_tropas, orden_ataque, tablero):
    fuerza_total = (combinacion_tropas[0] * fuerza_tropas['infanteria'] +
                    combinacion_tropas[1] * fuerza_tropas['caballeria'] +
                    combinacion_tropas[2] * fuerza_tropas['artilleria'])
    resultado = {'combinacion': combinacion_tropas, 'orden': orden_ataque, 'exito': True, 'territorios_conquistados': 0}
    for territorio in orden_ataque:
        if fuerza_total >= tablero[territorio]['defensa']:
            fuerza_total -= tablero[territorio]['defensa']
            resultado['territorios_conquistados'] += 1
        else:
            resultado['exito'] = False
            break
    return resultado

# Estrategia: priorizar tropas según el tipo de terreno
def ajustar_tropas_terreno(territorios, combinacion, tablero):
    estrategia = []
    for territorio in territorios:
        tipo = tablero[territorio].get('tipo', 'plano')
        if tipo == 'plano':
            estrategia.append(('caballeria', combinacion[1]))  # Priorizar caballería
        elif tipo == 'montaña':
            estrategia.append(('infanteria', combinacion[0]))  # Priorizar infantería
        elif tipo == 'fortaleza':
            estrategia.append(('artilleria', combinacion[2]))  # Priorizar artillería
    return estrategia

# Entrada personalizada de parámetros
def entrada_personalizada():
    global max_puntos, tablero, fuerza_tropas
    max_puntos = int(input("Introduce el máximo de puntos disponibles: "))
    fuerza_tropas['infanteria'] = int(input("Introduce la fuerza de infantería: "))
    fuerza_tropas['caballeria'] = int(input("Introduce la fuerza de caballería: "))
    fuerza_tropas['artilleria'] = int(input("Introduce la fuerza de artillería: "))
    
    tablero.clear()
    num_territorios = int(input("Introduce el número de territorios enemigos: "))
    for i in range(1, num_territorios + 1):
        defensa = int(input(f"Introduce la fuerza de defensa del territorio {i}: "))
        tipo = input(f"Introduce el tipo de terreno del territorio {i} (plano/montaña/fortaleza): ").lower()
        tablero[i] = {'defensa': defensa, 'tipo': tipo}

# Main
if __name__ == "__main__":
    # Fuerza de los territorios enemigos iniciales
    tablero = {
        1: {'defensa': 10, 'tipo': 'plano'},
        2: {'defensa': 15, 'tipo': 'montaña'},
        3: {'defensa': 12, 'tipo': 'fortaleza'}
    }

    # Generar combinaciones y permutaciones iniciales
    combinaciones_tropas = generar_combinaciones_tropas(max_puntos)
    permutaciones_ataques = generar_permutaciones_ataques(tablero.keys(), regla_debil=True, tablero=tablero)

    # Evaluar todas las combinaciones y órdenes
    resultados = []
    for combinacion in combinaciones_tropas:
        for orden in permutaciones_ataques:
            resultado = evaluar_combinacion(combinacion, orden, tablero)
            resultados.append(resultado)

    # Encontrar la mejor combinación (maximizar conquistas)
    mejor_resultado = max(resultados, key=lambda x: x['territorios_conquistados'])
    estrategia_tropas = ajustar_tropas_terreno(mejor_resultado['orden'], mejor_resultado['combinacion'], tablero)

    # Mostrar resultados
    print(f"Combinaciones posibles de tropas: {combinaciones_tropas}")
    print(f"Permutaciones posibles del orden de ataque: {permutaciones_ataques}")
    print(f"Resultados exitosos: {[r for r in resultados if r['exito']]}")
    print(f"Mejor combinación: {mejor_resultado}")
    print(f"Estrategia de tropas según terreno: {estrategia_tropas}")

    # Input de datos personalizado por el usuario
    opcion = input("¿Quieres probar con entrada personalizada? (s/n): ").lower()
    if opcion == 's':
        entrada_personalizada()
        combinaciones_tropas = generar_combinaciones_tropas(max_puntos)
        permutaciones_ataques = generar_permutaciones_ataques(tablero.keys(), regla_debil=True, tablero=tablero)
        resultados = []
        for combinacion in combinaciones_tropas:
            for orden in permutaciones_ataques:
                resultado = evaluar_combinacion(combinacion, orden, tablero)
                resultados.append(resultado)
        mejor_resultado = max(resultados, key=lambda x: x['territorios_conquistados'])
        estrategia_tropas = ajustar_tropas_terreno(mejor_resultado['orden'], mejor_resultado['combinacion'], tablero)
        print(f"Resultados exitosos con entrada personalizada: {[r for r in resultados if r['exito']]}")
        print(f"Mejor combinación: {mejor_resultado}")
        print(f"Estrategia de tropas según terreno: {estrategia_tropas}")
