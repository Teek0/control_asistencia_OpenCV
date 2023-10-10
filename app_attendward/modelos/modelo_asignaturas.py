class Asignatura:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.codigo = data['codigo']
        self.creado=data['creado']
        self.editado=data['editado']