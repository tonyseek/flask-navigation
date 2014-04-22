from flask import Flask, render_template
from flask.ext.navigation import Navigation


app = Flask()
nav = Navigation(app)

navbar = nav.Bar('top', [
    nav.Item(u'Home', endpoint='home'),
    nav.Item(u'Latest Article', endpoint='article', args=lambda: {'aid': 1}),
    nav.Item(u'More', endpoint='more', url='//example.com/more'),
])


@navbar.initializer
def init_navbar(nav):
    # yield items from database here
    def yield_items():
        for i in range(2):
            external_url = '//example.com/x/%d' % i
            yield nav.Item('X:%d' % i, endpoint='x-serial', url=external_url)
    # extend your bar
    nav['top'].extend(yield_items(), after_endpoint='article')


@app.route('/')
def home():
    return render_template('simple/home.html')


@app.route('/article/<int:aid>')
def article(aid):
    return render_template('simple/article.html', aid=aid)
