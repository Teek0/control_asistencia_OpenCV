class Seccion:
    def __init__(self, data):
        self.id = data['id']
        self.seccion = data['seccion']
        self.hora_inicio = data['hora_inicio']
        self.hora_fin = data['hora_fin']
        self.creado=data['creado']
        self.editado=data['editado']
        self.id_asignatura=data['id_asignatura']