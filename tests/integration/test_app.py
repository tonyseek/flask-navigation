from pytest import fixture
from webtest import TestApp

from .app import create_app


@fixture
def app():
    app = create_app()
    return TestApp(app)


def test_app(app):
    r = app.get('/')
    assert r.status == '200 OK'
    assert 'Welcome' in r
    assert_navbar_exists(r)
    assert_active(r, 'Home')

    r = r.click('Latest News')
    assert r.status == '200 OK'
    assert 'News :: Page - 1' in r
    assert_navbar_exists(r)
    assert_active(r, 'Latest News')

    r = r.click('Special News')
    assert r.status == '200 OK'
    assert 'News :: Page - 42' in r
    assert_navbar_exists(r)
    assert_active(r, 'Special News')

    r = r.click('Home')
    assert r.status == '200 OK'
    assert 'Welcome' in r
    assert_navbar_exists(r)
    assert_active(r, 'Home')


def test_alias(app):
    r = app.get('/news/1024')
    assert r.status == '200 OK'
    assert 'News :: Page - 1024' in r
    assert_navbar_exists(r)
    assert_active(r, '')

    r = r.click('Back')
    assert r.status == '200 OK'
    assert 'Welcome' in r
    assert_navbar_exists(r)
    assert_active(r, 'Home')


def assert_navbar_exists(r):
    assert 'Home' in r
    assert 'Latest News' in r
    assert 'Special News' in r


def assert_active(r, text):
    assert r.pyquery('li.active > a').text().strip() == text
