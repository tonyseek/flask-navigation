from flask import Blueprint, render_template

from .ext import nav


bp = Blueprint('main', __name__)

navbar_top = nav.Bar('top', [
    nav.Item('Home', endpoint='main.index'),
    nav.Item('Latest News', endpoint='main.news', args={'page': 1}),
], alias={'index': nav.ItemReference('main.index')})


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/news/<int:page>')
def news(page):
    return render_template('news.html', page=page)
