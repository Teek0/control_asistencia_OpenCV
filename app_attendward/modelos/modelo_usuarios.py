from app_attendward.config.mysqlconnection import connectToMySQL
from app_attendward import BASE_DATOS
from flask import flash

class Usuario:
    def __init__(self, data):
        self.id_usuario=data['id_usuario']
        self.id_seccion=data['id_seccion']
        self.nombre=data['nombre']
        self.apellido=data['apellido']
        self.user=data['user']
        self.password=data['password']
        self.es_admin=data['es_admin']
        self.creado=data['creado']
        self.editado=data['editado']

    @classmethod
    def obtener_uno_con_user(cls,data):
        query = """
                SELECT *
                FROM usuarios
                WHERE user = %(user)s
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query,data)
        if len(resultado)==0:
            return None
        else:
            return Usuario(resultado[0])
    
    @classmethod
    def crear_uno(cls,data):
        query = """
                INSERT INTO usuarios(nombre,apellido,user,password,es_admin)
                VALUES (%(nombre)s,%(apellido)s,%(user)s,%(password)s,%(es_admin)s)
                """
        id_usuario = connectToMySQL(BASE_DATOS).query_db(query,data)
        return id_usuario
    
    """@staticmethod
    def validar_registro(data,usuario_existe):
        es_valido = True
        if len(data['nombre'])<2:
            es_valido = False
            flash("Tu nombre necesita al menos 2 carácteres","error_nombre")
        if len(data['apellido'])<2:
            es_valido = False
            flash("Tu apellido necesita al menos 2 carácteres","error_apellido")
        if not user_REGEX.match(data['user']):
            es_valido = False
            flash("Por favor ingresa un user válido.","error_user")
        if data['password'] != data['confirmacion_password']:
            es_valido = False
            flash("Tus passwords no coinciden, intenta nuevamente.","error_password")
        if usuario_existe != None:
            es_valido=False
            flash("Correo ya registrado.","error_user")

        return es_valido"""