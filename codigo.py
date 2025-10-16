from flask import Flask, render_template, request
import random

app = Flask(__name__)

PROB_CRUCE = 0.8  # Probabilidad de cruce
PROB_MUTACION = 0.1 # Probabilidad de mutacion

def algoritmo_genetico(L, tamano_poblacion, num_generaciones):
    generacion = generar_poblacion_inicial(L, tamano_poblacion)
    mejor_final = []

    for x in range(num_generaciones-1):
        poblacion_con_fitness = []
        for individuo in generacion:
            poblacion_con_fitness += [(individuo, adaptabilidad(individuo, L))]

        seleccionados = seleccion(poblacion_con_fitness)

        for i in range(len(seleccionados)):
            a = 0

        

        
        

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
    suma = sum(individuo)
    if suma <= L:
        return suma
    else:
        return 0
    
def seleccion(poblacion):
    seleccionados = []
    for i in poblacion:
        if i[1] > 0:
            seleccionados += [i[0]]
        
    return seleccionados

def cruce(padre1, padre2):
    if len(padre1) == 1 or len(padre2) == 1:
        return padre1, padre2
    
    punto = random.randint(1, min(len(padre1), len(padre2)) - 1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2
    
def mutacion(individuo, L):
    mutado = individuo
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


algoritmo_genetico(10, 15, 25)



@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/generar', methods=['POST'])
def generar():
    L = int(request.form['L'])
    tamano_poblacion = int(request.form['tamano_poblacion'])

    poblacion = generar_poblacion_inicial(L, tamano_poblacion)
    return render_template('resultado.html', poblacion=poblacion,L=L, tamano_poblacion=tamano_poblacion)

if __name__ == '__main__':
    app.run(debug=True)
