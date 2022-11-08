from main import create_app, db
from flask_migrate import Migrate, upgrade, init, stamp
from models import Articles

def deploy():
    app = create_app()
    app.app_context().push()
    db.create_all()
    # Migrate db to latest revision
    stamp()
    Migrate()
    upgrade()

deploy()