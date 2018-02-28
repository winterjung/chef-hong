#!/usr/bin/env python
import os

from flask_script import Manager, Shell

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    os.system('pytest tests')


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
