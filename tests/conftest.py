import json
import random
import string
from functools import wraps

import pytest

from app import create_app
from app import db as app_db
from app.api.chatter import chatter


@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    return app


@pytest.yield_fixture(scope='function')
def client(app, mocker):
    with app.test_client() as client:
        mocker.patch('app.api.chatter.logger')
        mocker.patch('app.api.menu.day_to_weekday', **{'return_value': 0})
        client = Client(client)
        yield client


@pytest.yield_fixture(scope='function')
def api_client(app):
    with app.test_client() as client:
        client.post = ensure_json(client.post)
        client.put = ensure_json(client.put)
        yield client


@pytest.yield_fixture(scope='function')
def db(client):
    app_db.create_all()
    yield app_db
    app_db.session.remove()
    app_db.drop_all()


class Client:
    def __init__(self, client):
        self.client = client

    def url(self, url):
        self.url = url
        return self

    def get(self):
        self.response = self.client.get(self.url)
        return Response(self.response)

    def post(self, *args):
        user_key = self.random_user()
        for content in args:
            payload = self.data(content, user_key)
            self.response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type='application/json'
            )

        return Response(self.response)

    def random_user(self, n=16):
        charset = string.ascii_uppercase + string.digits
        return ''.join(random.choices(charset, k=n))

    def data(self, content, user_key, message_type='text'):
        return {
            'user_key': user_key,
            'type': message_type,
            'content': content,
        }


class Response:
    def __init__(self, data):
        self.response = data
        self.json = self.response.json

    def status(self, code):
        assert self.response.status_code == code
        return self

    def contain(self, *args):
        for target in args:
            msg = self.json['message']
            text = msg.get('text', '')
            photo = msg.get('photo', {})
            button = msg.get('message_button', {})

            in_text = target in text
            in_photo = target in photo.get('url', '')
            in_button_label = target in button.get('label', '')
            in_button_url = target in button.get('url', '')

            assert any([in_text, in_photo, in_button_label, in_button_url])
        return self

    def msg(self, *args):
        for msg in (args):
            assert msg in self.json['message']
        return self

    def keyboard(self, buttons):
        assert buttons == self.json['keyboard']['buttons']
        return self

    def home(self):
        buttons = chatter.home().buttons
        assert buttons == self.json['keyboard']['buttons']
        return self


def ensure_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['content_type'] = kwargs.get('content_type', 'application/json')
        if kwargs['content_type'] == 'application/json':
            data = kwargs.get('data')
            kwargs['data'] = json.dumps(data)

        result = func(*args, **kwargs)
        return result
    return wrapper
