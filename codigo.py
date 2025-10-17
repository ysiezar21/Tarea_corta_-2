from flask import Flask, render_template, request
import random

app = Flask(__name__)

PROB_CRUCE = 0.8  # Probabilidad de cruce
PROB_MUTACION = 0.1 # Probabilidad de mutacion


# Entradas: 
#   L = Numero limite de la suma de cada individuo
#   tamano_poblacion = Cantidad de individuos que debe haber en cada generación
#   num_generaciones = Numero de generaciones que debe generar el algoritmo 
# Salidas:
#   lista_generaciones = Lista que contiene los individuos seleccionados como mejores de cada generacion.
#   [mejor_final, generacion_mejor_final] = Arreglo que contiene el mejor individuo encontrado durante el algoritmo y su generacion.
# Restricciones:
#   L debe ser mayor o igual a 1
#   El tamaño de la poblacion debe ser mayor o igual a 10
#   El minimo de generaciones es de 25
def algoritmo_genetico(L, tamano_poblacion, num_generaciones):
    generacion = generar_poblacion_inicial(L, tamano_poblacion)
    lista_generaciones = []
    mejor_final = generacion[0]
    generacion_mejor_final = 0

    for x in range(num_generaciones):
        seleccionados = []
        poblacion_con_fitness = []
        for individuo in generacion:
            adapt = adaptabilidad(individuo, L)
            poblacion_con_fitness += [[individuo, adapt]]

        seleccionados = seleccion(poblacion_con_fitness)

        lista_generaciones.append([ind[:] for ind in seleccionados])
        
        poblacion_cruzada = realizar_cruce(seleccionados)

        poblacion_mutada = []
        for individuo in poblacion_cruzada:
            poblacion_mutada += [mutacion(individuo, L)]
        
        generacion = poblacion_mutada
        generacion = completar_poblacion(generacion, L, tamano_poblacion)

        mejor_generacion = buscar_mejor(generacion, L)
        suma = sumar(mejor_generacion)

        if sumar(mejor_final) > L:
            mejor_final = mejor_generacion
            generacion_mejor_final = x + 1

        if suma <= L:
            if suma > sumar(mejor_final):
                mejor_final = mejor_generacion
                generacion_mejor_final = x + 1
            elif suma == sumar(mejor_final) and len(mejor_generacion) < len(mejor_final):
                mejor_final = mejor_generacion
                generacion_mejor_final = x + 1

    return lista_generaciones, [mejor_final, generacion_mejor_final]
        
# Entradas:
#   generacion = Lista de individuos de la generación actual
#   L = Numero limite de la suma
# Salidas:
#   res = Mejor individuo encontrado en la generación
# Restricciones:
#   La generación no debe estar vacía
def buscar_mejor(generacion, L):
    res = [0]
    for individuo in generacion:
        suma = sumar(individuo)
        if suma <= L:
            if suma > sumar(res):
                res = individuo
            elif suma == sumar(res) and len(res) > len(individuo):
                res = individuo
        else:
            if sumar(res) == 0:
                res = individuo
            elif suma < sumar(res):
                res = individuo
    return res

# Entradas:
#   L = Numero limite de la suma y de elementos por individuo
#   tamano_poblacion = Cantidad de individuos a generar
# Salidas:
#   poblacion = Lista de individuos generados aleatoriamente
# Restricciones:
#   L debe ser mayor o igual a 1
#   tamano_poblacion debe ser mayor o igual a 10
def generar_poblacion_inicial(L, tamano_poblacion):
    poblacion = []
    
    for _ in range(tamano_poblacion):
        longitud = random.randint(1, L)
        individuo = []
        for _ in range(longitud):
            individuo += [random.randint(1, L)] 
        poblacion.append(individuo)
    
    return poblacion

# Entradas:
#   poblacion = Lista de individuos actual
#   L = Numero limite de la suma
#   tamano_poblacion = Tamaño objetivo de la población
# Salidas:
#   poblacion = Población ajustada al tamaño deseado
# Restricciones:
#   L debe ser mayor o igual a 1
#   tamano_poblacion debe ser mayor o igual a 10
def completar_poblacion(poblacion, L, tamano_poblacion):
    largo = len(poblacion)

    if largo < tamano_poblacion:
        for i in range(largo, tamano_poblacion):
            longitud = random.randint(1, L)
            individuo = []
            for _ in range(longitud):
                individuo += [random.randint(1, L)] 
            poblacion.append(individuo)
    else:
        while len(poblacion) > tamano_poblacion:
            poblacion = poblacion[:-1]
    
    return poblacion

# Entradas:
#   individuo = Lista de números que representa un individuo
#   L = Numero limite de la suma
# Salidas:
#   Valor de adaptabilidad del individuo (suma si cumple restricción, 0 en caso contrario)
# Restricciones:
#   L debe ser mayor o igual a 1
def adaptabilidad(individuo, L):
    suma = sumar(individuo)
    if suma <= L and suma > 0:
        return suma
    else:
        return 0

# Entradas:
#   poblacion = Lista de tuplas [individuo, fitness]
# Salidas:
#   seleccionados = Lista de individuos seleccionados con fitness mayor a 0
# Restricciones:
#   Cada elemento de población debe ser una tupla [individuo, fitness]
def seleccion(poblacion):
    seleccionados = []
    for i in poblacion:
        if i[1] > 0 and i[0] not in seleccionados:
            seleccionados = seleccionados + [i[0]]
        
    return seleccionados

# Entradas:
#   poblacion = Lista de individuos padres
# Salidas:
#   poblacion_cruzada = Lista de individuos hijos resultantes del cruce
# Restricciones:
#   La población no debe estar vacía
#   PROB_CRUCE debe estar definida globalmente
def realizar_cruce(poblacion):
    poblacion_cruzada = []
    i = 0
    for padre1 in poblacion:
        i = random.randint(0, len(poblacion)-1)
        padre2 = poblacion[i]
        if len(padre1) == 1 or len(padre2) == 1:
            poblacion_cruzada += [padre1[:], padre2[:]]
        elif random.random() < PROB_CRUCE:
            punto = random.randint(1, min(len(padre1), len(padre2)) - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            poblacion_cruzada += [hijo1, hijo2]
        else:
            poblacion_cruzada += [padre1[:], padre2[:]]
    return poblacion_cruzada
    
# Entradas:
#   individuo = Lista de números que representa un individuo
#   L = Numero limite de la suma
# Salidas:
#   mutado = Individuo resultante después de aplicar mutación
# Restricciones:
#   L debe ser mayor o igual a 1
#   PROB_MUTACION debe estar definida globalmente
def mutacion(individuo, L):
    mutado = individuo[:]
    for i in range(len(individuo)):
        if random.random() < PROB_MUTACION:
            num = random.randint(1, L)
            if num in mutado:
                mutado.remove(num)
            else:
                mutado.append(num)
    while len(mutado) > L:
        mutado = mutado[:-1]
    return mutado

# Entradas:
#   lista = Lista de números a sumar
# Salidas:
#   res = Suma total de los elementos de la lista
# Restricciones:
#   Ninguna
def sumar(lista):
    res = 0
    for x in lista:
        res += x
    return res 

# Rutas a la parte grafica y ejecucion del sistema.
@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/ejecutar_algoritmo', methods=['POST'])
def ejecutar_algoritmo():
    L = int(request.form['L'])
    tamano_poblacion = int(request.form['tamano_poblacion'])
    num_generaciones = int(request.form.get('num_generaciones', 25))

    # Ejecutar el algoritmo genético
    historico, mejor_final = algoritmo_genetico(L, tamano_poblacion, num_generaciones)
    
    return render_template('resultado.html', historico=historico, mejor_final=mejor_final, L=L, tamano_poblacion=tamano_poblacion, num_generaciones=num_generaciones)
    
if __name__ == '__main__':
    app.run(debug=True)
