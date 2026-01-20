from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, News, Comment
from forms import LoginForm, RegisterForm, NewsForm, CommentForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asamitaka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('index.html', news=news, title="All News")


@app.route('/sports')
def sports():
    news = News.query.filter_by(category='sports').order_by(News.created_at.desc()).all()
    return render_template('sports.html', news=news, title='Sports News')


@app.route('/culture')
def culture():
    news = News.query.filter_by(category='culture').order_by(News.created_at.desc()).all()
    return render_template('culture.html', news=news, title='Culture News')


@app.route('/arts')
def arts():
    news = News.query.filter_by(category='arts').order_by(News.created_at.desc()).all()
    return render_template('arts.html', news=news, title='Arts News')


@app.route('/business')
def business():
    news = News.query.filter_by(category='business').order_by(News.created_at.desc()).all()
    return render_template('business.html', news=news, title='Business News')


@app.route('/innovation')
def innovation():
    news = News.query.filter_by(category='innovation').order_by(News.created_at.desc()).all()
    return render_template('innovation.html', news=news, title='Innovation News')


@app.route('/earth')
def earth():
    news = News.query.filter_by(category='earth').order_by(News.created_at.desc()).all()
    return render_template('earth.html', news=news, title='Earth News')


@app.route('/travel')
def travel():
    news = News.query.filter_by(category='travel').order_by(News.created_at.desc()).all()
    return render_template('travel.html', news=news, title='Travel News')


@app.route('/health')
def health():
    news = News.query.filter_by(category='health').order_by(News.created_at.desc()).all()
    return render_template('health.html', news=news, title='Health News')


@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_detail(news_id):
    news = News.query.get_or_404(news_id)
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            text=form.text.data,
            user_id=current_user.id,
            news_id=news.id
        )
        db.session.add(comment)
        db.session.commit()
        

    return render_template('news_details.html', news=news, form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    form = NewsForm()
    if form.validate_on_submit():
        file = form.image.data

        if not file:
            return render_template('addnews.html', form=form)

        filename = secure_filename(file.filename)
        os.makedirs("static/uploads", exist_ok=True)
        file.save(os.path.join("static/uploads", filename))

        news = News(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            image=filename

        )
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addnews.html', form=form)


@app.route('/delete/<int:news_id>')
@login_required
def delete_news(news_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))

    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return redirect(url_for('register'))

        username = form.username.data
        is_admin = 0
        if username.lower() == 'admin':
            is_admin = 1

        user = User(username=username, is_admin=is_admin)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
