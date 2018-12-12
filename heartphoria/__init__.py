from flask import Flask

from werkzeug.utils import find_modules, import_string

app = Flask(__name__)
app.secret_key = b'\xc44\xe9\xaf\x7f\xe0\xd2we\xc8\xbc\xda\x02sm\x16'

from heartphoria import db
db.init_app()

for name in find_modules('heartphoria.blueprints'):
    mod = import_string(name)
    if hasattr(mod, 'blueprint'):
        app.register_blueprint(mod.blueprint)
