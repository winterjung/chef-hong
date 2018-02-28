import json
import random
import string
import pytest
from flask import url_for


def random_user(n=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def data(content, user_key=None, message_type='text'):
    return {
        'user_key': user_key if user_key else random_user(),
        'type': message_type,
        'content': content,
    }


def post(client, url, data):
    return client.post(url,
                       data=json.dumps(data),
                       content_type='application/json')


class TestKeyboard:
    def test_keyboard(self, client):
        url = url_for('api.keyboard')
        res = client.get(url)

        assert res.status_code == 200
        assert res.json['type'] == 'buttons'
        assert res.json['buttons'] == ['식단 보기', '다른 기능']


class TestMessage:
    def home(self):
        return ['식단 보기', '다른 기능']

    def test_menu(self, client):
        url = url_for('api.message')
        payload = data('식단 보기')
        res = post(client, url, payload)

        assert res.status_code == 200
        assert '구현중' in res.json['message']['text']
        assert res.json['keyboard']['type'] == 'buttons'
        assert res.json['keyboard']['buttons'] == self.home()

    def test_etc(self, client):
        url = url_for('api.message')
        payload = data('다른 기능')
        res = post(client, url, payload)

        assert res.status_code == 200
        assert '안녕하세요' in res.json['message']['text']
        assert res.json['keyboard']['type'] == 'buttons'
        assert res.json['keyboard']['buttons'] == ['자기소개', '추가될 기능', '취소']

    def test_intro(self, client):
        url = url_for('api.message')
        user_key = random_user()
        payload = data('다른 기능', user_key)
        post(client, url, payload)
        payload = data('자기소개', user_key)
        res = post(client, url, payload)

        assert res.status_code == 200
        assert '여기서 개발' in res.json['message']['text']
        assert 'message_button' in res.json['message']
        assert res.json['keyboard']['type'] == 'buttons'
        assert res.json['keyboard']['buttons'] == self.home()

    def test_roadmap(self, client):
        url = url_for('api.message')
        user_key = random_user()
        payload = data('다른 기능', user_key)
        post(client, url, payload)
        payload = data('추가될 기능', user_key)
        res = post(client, url, payload)

        assert res.status_code == 200
        assert '다양한 기능' in res.json['message']['text']
        assert 'message_button' in res.json['message']
        assert res.json['keyboard']['type'] == 'buttons'
        assert res.json['keyboard']['buttons'] == self.home()

    def test_cancel(self, client):
        url = url_for('api.message')
        user_key = random_user()
        payload = data('다른 기능', user_key)
        post(client, url, payload)
        payload = data('취소', user_key)
        res = post(client, url, payload)

        assert res.status_code == 200
        assert '취소' in res.json['message']['text']
        assert res.json['keyboard']['type'] == 'buttons'
        assert res.json['keyboard']['buttons'] == self.home()

    def test_invalid(self, client):
        url = url_for('api.message')
        payload = data('자기소개')

        with pytest.raises(ValueError) as exc_info:
            post(client, url, payload)
        assert 'no matching function' in str(exc_info.value)
