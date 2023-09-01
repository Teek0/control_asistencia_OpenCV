class alumno:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.ruta_archivo = data['ruta_archivo']
        self.creado=data['creado']
        self.editado=data['editado']