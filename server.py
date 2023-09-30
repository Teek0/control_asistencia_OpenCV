from app_attendward.controladores import controlador_alumnos,controlador_cursos
from app_attendward import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)