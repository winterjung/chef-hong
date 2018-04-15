from flask import url_for


def test_chef_cache(api_client):
    url = url_for('util.chef_cache')
    res = api_client.get(url)
    assert res.status_code == 200
    assert isinstance(res.json, dict)


def test_sentry(api_client, mocker):
    url = url_for('util.test_sentry')
    mocker.patch('app.util.views.sentry')
    res = api_client.get(url)
    assert res.status_code == 200
    assert 'invalid literal for int() with base 10' in res.json['msg']
