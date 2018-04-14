from app.models import User


def test_user_create(db):
    user = User(user_key='test', nickname='guest')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.user_key == 'test'
    assert user.nickname == 'guest'
