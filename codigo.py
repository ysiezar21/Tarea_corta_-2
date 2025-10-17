from flask import Flask, render_template, request
import random

app = Flask(__name__)

PROB_CRUCE = 0.8  # Probabilidad de cruce
PROB_MUTACION = 0.1 # Probabilidad de mutacion

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

def generar_poblacion_inicial(L, tamano_poblacion):
    poblacion = []
    
    for _ in range(tamano_poblacion):
        longitud = random.randint(1, L)
        individuo = []
        for _ in range(longitud):
            individuo += [random.randint(1, L)] 
        poblacion.append(individuo)
    
    return poblacion

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

def adaptabilidad(individuo, L):
    suma = sumar(individuo)
    if suma <= L and suma > 0:
        return suma
    else:
        return 0
    
def seleccion(poblacion):
    seleccionados = []
    for i in poblacion:
        if i[1] > 0 and i[0] not in seleccionados:
            seleccionados = seleccionados + [i[0]]
        
    return seleccionados

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

def sumar(lista):
    res = 0
    for x in lista:
        res += x
    return res 

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
