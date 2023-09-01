from flask import render_template
from app_attendward import app

@app.route('/', methods=['GET'])
def desplegar_lista_de_cursos():
    return render_template('lista_cursos.html')