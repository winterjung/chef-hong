import json
import random
import string
import pytest
from flask import url_for


class TestKeyboard:
    def test_keyboard(self, client, mocker):
        mocker.patch('app.api.chatter.logger')
        url = url_for('api.keyboard')
        res = Client(client).url(url).get()
        assert res.json['buttons'] == ['오늘의 식단', '다른 식단 보기', '다른 기능']


class TestMessage:
    @classmethod
    @pytest.fixture(autouse=True)
    def set_up(self, client, mocker):
        mocker.patch('app.api.chatter.logger')
        mocker.patch('app.api.menu.day_to_weekday', **{'return_value': 0})
        url = url_for('api.message')
        self.client = Client(client).url(url)

    def test_today(self):
        res = self.client.post('오늘의 식단')
        (res
            .status(200)
            .contain('오늘의 간략한 식단', '식당')
            .keyboard(['전체 식단', '점심', '신기숙사', '취소']))

    def test_other(self, client):
        res = self.client.post('다른 식단 보기')
        (res
            .status(200)
            .contain('내일의 간략한 식단', '식당')
            .keyboard(['내일의 전체 식단', '내일의 신기숙사', '이번주 식단', '취소']))

    def test_etc(self, client):
        res = self.client.post('다른 기능')
        (res
            .status(200)
            .contain('안녕하세요')
            .msg('text')
            .keyboard(['자기소개', '추가될 기능', '취소']))

    def test_today_step2(self, client):
        res = self.client.post('오늘의 식단', '전체 식단')
        (res
            .status(200)
            .contain('아침', '점심', '저녁')
            .home())

        res = self.client.post('오늘의 식단', '점심')
        (res
            .status(200)
            .contain('점심')
            .home())

        res = self.client.post('오늘의 식단', '신기숙사')
        (res
            .status(200)
            .contain('기숙사')
            .home())

    def test_other_step2(self, client):
        res = self.client.post('다른 식단 보기', '내일의 전체 식단')
        (res
            .status(200)
            .contain('아침', '점심', '저녁')
            .home())

        res = self.client.post('다른 식단 보기', '내일의 신기숙사')
        (res
            .status(200)
            .contain('아침', '점심', '저녁', '기숙사')
            .home())

        res = self.client.post('다른 식단 보기', '이번주 식단')
        (res
            .status(200)
            .contain('이번주')
            .home())

    def test_etc_intro(self, client):
        res = self.client.post('다른 기능', '자기소개')
        (res
            .status(200)
            .msg('text')
            .home())

    def test_etc_roadmap(self, client):
        res = self.client.post('다른 기능', '추가될 기능')
        (res
            .status(200)
            .msg('text')
            .home())

    def test_cancel(self, client):
        res = self.client.post('오늘의 식단', '취소')
        (res
            .status(200)
            .contain('취소하셨습니다')
            .msg('text')
            .home())


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
        buttons = ['오늘의 식단', '다른 식단 보기', '다른 기능']
        assert buttons == self.json['keyboard']['buttons']
        return self
