from flask import render_template
from app_attendward import app

@app.route('/cursos', methods=['GET'])
def get_all_cursos():
    return render_template('cursos.html')