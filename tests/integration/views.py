from flask import Blueprint, current_app, render_template

from .ext import nav


bp = Blueprint('main', __name__)

navbar_top = nav.Bar('top', [
    nav.Item('Home', 'main.index'),
    nav.Item('Latest News', 'main.news', {'page': 1}),
], alias={'index': nav.ItemReference('main.index')})


@navbar_top.initializer
def initialize_navbar_top(nav):
    top = nav['top']
    if len(top.items) > 2:
        return
    args = {'page': current_app.config['NEWS_SPECIAL_PAGE']}
    item = nav.Item('Special News', 'main.news', args)
    top.items.append(item)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/news/<int:page>')
def news(page):
    return render_template('news.html', page=page)
