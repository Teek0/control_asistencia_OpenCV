from flask import Flask
import re

app = Flask(__name__)
app.secret_key = "esto es secreto"

BASE_DATOS = "attend_bd"

NOMBRE_REGEX = re.compile(r'^[a-zA-Z ]+$')