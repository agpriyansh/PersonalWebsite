from flask import Flask, render_template, redirect, request, flash, Response, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

website = Flask(__name__)
website.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'priyanshagrawal385@gmail.com',
    MAIL_PASSWORD = 'i_fckn_love_htb'
)
mail = Mail(website)
website.secret_key = 'eb3e92e0439bd515e3a8a7c74bb72c0f'
website.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ubuntu:7H15_u53r_15_4_7h3_W3B5173_d474@localhost/website'
database = SQLAlchemy(website)
login_info = {
    'user':'agpriyansh',
    'passwd':'pripri@@1301'
}

class Blog(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    desc = database.Column(database.String(255), nullable=False)
    page = database.Column(database.String(255), nullable=False)
    slug = database.Column(database.String(255), nullable=False)

class htb(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    category = database.Column(database.String(255), nullable=False)
    image = database.Column(database.String(255), nullable=False)
    page = database.Column(database.String(255), nullable=False)
    slug = database.Column(database.String(255), nullable=False)


@website.route('/', methods = ['GET'])
def index():
    return redirect('/home')

@website.route('/home', methods = ['GET'])
def home():
    all_blogs = Blog.query.filter_by().all()
    all_htb = htb.query.filter_by().all()
    all_blogs.reverse()
    all_htb.reverse()
    return render_template('home.html', blog=all_blogs[0:4], htb=all_htb[0:4])

@website.route('/hackthebox', methods = ['GET'])
def all_hackthebox():
    all_htb = htb.query.filter_by().all()
    all_htb.reverse()
    return render_template('hackthebox.html', htb=all_htb)

@website.route('/hackthebox/<string:slug>', methods = ['GET'])
def hackthebox(slug):
    box = htb.query.filter_by(slug=slug).first()
    return render_template(box.page, box=box)

@website.route('/add-hackthebox', methods = ['POST'])
def add_hackthebox():
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        name = request.form.get('name')
        category = request.form.get('category')
        slug = request.form.get('slug')
        image = request.form.get('image')
        html = request.form.get('html')

        new_htb = htb(name=name, category=category, image=image, page=html, slug=slug)
        database.session.add(new_htb)
        database.session.commit()

        return redirect('/dashboard')
    else:
        return redirect('/agpriyansh')

@website.route('/delete-hackthebox/<string:id>', methods = ['GET'])
def delete_hackthebox(id):
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        box = htb.query.filter_by(id=id).first()
        database.session.delete(box)
        database.session.commit()

        return redirect('/dashboard')
    else:
        return redirect('/agpriyansh')

@website.route('/blog', methods = ['GET'])
def all_blogs():
    all_blogs = Blog.query.filter_by().all()
    all_blogs.reverse()
    return render_template('blog.html', blog=all_blogs)

@website.route('/blog/<string:slug>', methods = ['GET'])
def blogs(slug):
    try:
        blog = Blog.query.filter_by(slug=slug).first()
        return render_template(blog.page)
    except:
        return render_template('404.html')

@website.route('/add-blog', methods = ['POST'])
def add_blog():
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        name = request.form.get('name')
        slug = request.form.get('slug')
        desc = request.form.get('desc')
        html = request.form.get('html')

        new_blog = Blog(name=name, slug=slug, desc=desc, page=html)
        database.session.add(new_blog)
        database.session.commit()

        return redirect('/dashboard')
    else:
        return redirect('/agpriyansh')

@website.route('/delete-blog/<string:id>', methods = ['GET'])
def delete_blog(id):
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        blog = Blog.query.filter_by(id=id).first()
        database.session.delete(blog)
        database.session.commit()
        return redirect('/dashboard')
    else:
        return redirect('/agpriyansh')


@website.route('/contact', methods = ['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        mail.send_message('Message From Website',
                            sender=name,
                            recipients=['priyanshagrawal224@gmail.com','priyanshagrawal@live.in'],
                            body='Subject - ' + subject + "\n\nMessage - " + message + "\n\nEmail - " + email + "\n\nBy - " + name
                            )

        return redirect('/home')

@website.route('/agpriyansh', methods = ['GET', 'POST'])
def agpriyansh():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = request.form.get('user')
        passwd = request.form.get('passwd')
        if user == login_info['user'] and passwd == login_info['passwd']:
            session['logged_in'] = user
            mail.send_message('WEBSITE ALERT !!!!',
                            sender='Website Priyansh',
                            recipients=['priyanshagrawal224@gmail.com','priyanshagrawal@live.in'],
                            body='DID YOU JUST LOG IN TO YOUR WEBSITE ???\nIF YES, IGNORE THIS EMAIL.\nIF YOU DIDN\'T, YOU KNOW WHAT TO DO :|'
                            )
            return redirect('/dashboard')
        else:
            return render_template('login.html', message='Login Failed :(')

@website.route('/dashboard', methods = ['GET'])
def dashboard():
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        all_blogs = Blog.query.filter_by().all()
        all_hackthebox = htb.query.filter_by().all()
        return render_template('dashboard.html', blog=all_blogs, htb=all_hackthebox)
    else:
        return redirect('/agpriyansh')

@website.route('/test')
def test():
    return render_template('base.html')

@website.route('/logout', methods = ['GET'])
def logout():
    if 'logged_in' in session and session['logged_in'] == login_info['user']:
        session.pop('logged_in')
        return redirect('/home')
    else:
        return redirect('/home')

