from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import *

migrate = Migrate(app, db)

manager = Manager(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
