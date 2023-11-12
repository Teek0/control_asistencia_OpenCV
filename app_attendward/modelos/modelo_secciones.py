from app_attendward.config.mysqlconnection import connectToMySQL

class Seccion:
    def __init__(self, data):
        self.id_seccion = data['id_seccion']
        self.id_docente = data['id_docente']
        self.id_asignatura = data['id_asignatura']
        self.seccion = data['seccion']
        self.hora_inicio = data['hora_inicio']
        self.hora_fin = data['hora_fin']
        self.creado=data['creado']
        self.editado=data['editado']