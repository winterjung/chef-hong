import pytest
from flask import url_for


class TestKeyboard:
    def test_keyboard(self, client):
        url = url_for('api.keyboard')
        res = client.url(url).get()
        assert res.json['buttons'] == ['오늘의 식단', '다른 식단 보기', '다른 기능']


class TestMessage:
    @classmethod
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        url = url_for('api.message')
        self.client = client.url(url)

    def test_today(self):
        res = self.client.post('오늘의 식단')
        (res
            .status(200)
            .contain('오늘의 간략한 식단', '식당')
            .keyboard(['전체 식단', '점심', '신기숙사', '취소']))

    def test_other(self):
        res = self.client.post('다른 식단 보기')
        (res
            .status(200)
            .contain('내일의 간략한 식단', '식당')
            .keyboard(['내일의 전체 식단', '내일의 신기숙사', '이번주 식단', '취소']))

    def test_etc(self):
        res = self.client.post('다른 기능')
        (res
            .status(200)
            .contain('안녕하세요')
            .msg('text')
            .keyboard(['자기소개', '추가될 기능', '취소']))

    def test_today_step2(self):
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

    def test_other_step2(self):
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

    def test_etc_intro(self):
        res = self.client.post('다른 기능', '자기소개')
        (res
            .status(200)
            .msg('text')
            .home())

    def test_etc_roadmap(self):
        res = self.client.post('다른 기능', '추가될 기능')
        (res
            .status(200)
            .msg('text')
            .home())

    def test_cancel(self):
        res = self.client.post('오늘의 식단', '취소')
        (res
            .status(200)
            .contain('취소하셨습니다')
            .msg('text')
            .home())


def test_add_firend(api_client):
    url = url_for('api.add_friend')
    res = api_client.post(url)
    assert res.status_code == 200
    assert res.json['message'] == 'SUCCESS'


def test_block_friend(api_client):
    url = url_for('api.block_friend', key='test_user_key')
    res = api_client.delete(url)
    assert res.status_code == 200
    assert res.json['message'] == 'SUCCESS'


def test_exit_friend(api_client):
    url = url_for('api.exit_friend', key='test_user_key')
    res = api_client.delete(url)
    assert res.status_code == 200
    assert res.json['message'] == 'SUCCESS'
