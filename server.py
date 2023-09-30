from app_attendward.controladores import controlador_alumnos,controlador_cursos,controlador_usuarios,controlador_asistencias
from app_attendward import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)