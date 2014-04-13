from flask import Flask, Blueprint, render_template
from flask.ext.navigation import Navigation


app = Flask(__name__)
nav = Navigation(app)

pocket = Blueprint(__name__, 'pocket', url_prefix='/pocket')
app.register_blueprint(pocket)

navbar = nav.Bar('top', [
    nav.Item(u'Home', endpoint='home'),
    nav.Item(u'Pocket', endpoint='pocket')
])

pocket_navbar = nav.Bar('pocket', [
    nav.Item(u'Back', endpoint='pocket'),
    nav.Item(u'Article', endpoint='pocket.article'),
    nav.Item(u'Video', endpoint='pocket.video'),
], alias={'back': nav.ItemReference('pocket')})


@app.route('/')
def home():
    return render_template('nested/home.html')


@app.route('/pocket')
def pocket():
    return render_template('nested/pocket.html')


@pocket.route('/article')
def article():
    return render_template('nested/pocket-article.html')


@pocket.route('/video')
def video():
    return render_template('nested/pocket-video.html')
