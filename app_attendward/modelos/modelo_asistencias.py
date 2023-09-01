class asistencia:
    def __init__(self, data):
        self.id = data['id']
        self.id_alumno = data['id_alumno']
        self.id_curso = data['id_curso']
        self.fecha = data['fecha']
        self.asiste = data['asiste']
