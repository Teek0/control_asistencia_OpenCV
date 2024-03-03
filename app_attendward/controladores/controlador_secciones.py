from flask import render_template
from app_attendward import app
from app_attendward.config.mysqlconnection import connectToMySQL

@app.route('/cursos', methods=['GET'])
def get_all_cursos():
    mysql = connectToMySQL('attend_bd')
    data = mysql.query_db("SELECT secciones.*, asignaturas.nombre AS nombre_asignatura FROM secciones JOIN asignaturas ON asignaturas.id_asignatura = secciones.id_asignatura;")
    mysql.close_connection()
    return render_template('cursos.html', cursos=data)

@app.route('/alumnos/<int:section_id>', methods=['GET'])
def get_alumnos_by_section(section_id):
    mysql = connectToMySQL('attend_bd')
    # Consulta para obtener los datos de la sección y la asignatura
    section_query = "SELECT secciones.*, asignaturas.nombre AS nombre_asignatura FROM secciones JOIN asignaturas ON asignaturas.id_asignatura = secciones.id_asignatura WHERE secciones.id_seccion = %s;"
    section_data = mysql.query_db(section_query, (section_id,))
    # Consulta para obtener los datos de los alumnos
    alumnos_query = "SELECT alumnos.* FROM alumnos JOIN inscritos ON inscritos.id_alumno = alumnos.id_alumno WHERE inscritos.id_seccion = %s;"
    alumnos_data = mysql.query_db(alumnos_query, (section_id,))
    # Cerrar la conexión manualmente
    mysql.close_connection()
    return render_template('alumnos.html', seccion=section_data[0], alumnos=alumnos_data)