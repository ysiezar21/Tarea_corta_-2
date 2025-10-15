from flask import Flask, render_template, request
import random

app = Flask(__name__)

eleccion = []

def generar_poblacion(L, tamano_poblacion):
    if L < 1:
        raise ValueError("L debe ser >= 1")
    if tamano_poblacion < 10:
        raise ValueError("El tamaño de población debe ser >= 10")
    
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
    
    return poblacion

def generaciones(num_generaciones):
    
    for x in range(num_generaciones):
        a=0 


@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/generar', methods=['POST'])
def generar():
    L = int(request.form['L'])
    tamano_poblacion = int(request.form['tamano_poblacion'])

    poblacion = generar_poblacion(L, tamano_poblacion)
    return render_template('resultado.html', poblacion=poblacion,L=L, tamano_poblacion=tamano_poblacion)

if __name__ == '__main__':
    app.run(debug=True)
    