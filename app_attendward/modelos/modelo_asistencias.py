class Asistencia:
    def __init__(self, data):
        self.id_alumno = data['id_alumno']
        self.id_curso = data['id_curso']
        self.fecha = data['fecha']
        self.asiste = data['asiste']

