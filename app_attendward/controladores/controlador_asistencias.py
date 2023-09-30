from flask import render_template
from app_attendward import app

@app.route('/captura_asistencia', methods=['GET'])
def get_all_alumnos():
    return render_template('captura_asistencia.html')