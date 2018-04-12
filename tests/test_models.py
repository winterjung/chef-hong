from pony.orm import db_session

from app.models import User


@db_session
def test_user_create(db):
    User(user_key='test', nickname='guest')
    db.commit()
    user = User.get(user_key='test')
    assert user is not None
    assert user.nickname == 'guest'
