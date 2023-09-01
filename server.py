from app_attendward.controladores import controlador_alumnos,controlador_cursos
''',controlador_profesores,controlador_asistencias,controlador_reportes'''
from app_attendward import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)