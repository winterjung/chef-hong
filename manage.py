#!/usr/bin/env python
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db, models
from app.api import chatter

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, chatter=chatter, models=models)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    pass


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    pass


if __name__ == '__main__':
    manager.run()
