from app_attendward.config.mysqlconnection import connectToMySQL

class Docente:
    def __init__(self, data):
        self.id_docente=data['id_docente']
        self.nombre=data['nombre']
        self.apellido=data['apellido']
        self.user=data['user']
        self.password=data['password']
        self.creado=data['creado']
        self.editado=data['editado']
