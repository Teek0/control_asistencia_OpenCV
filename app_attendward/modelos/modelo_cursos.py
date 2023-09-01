class curso:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.seccion = data['seccion']
        self.creado=data['creado']
        self.editado=data['editado']