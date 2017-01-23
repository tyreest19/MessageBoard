from Database import Database
import os
from flask_login import LoginManager
from flask import escape
from flask import redirect
from flask import request
from flask import Flask
from flask import render_template
from flask import session
from models.User import User
from models.Post import Post
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static')
login_manager = LoginManager()
login_manager.init_app(app)
users_database = Database('MessageBoard','users','mongodb://127.0.0.1:27017')
posts_database = Database('MessageBoard', 'posts', 'mongodb://127.0.0.1:27017')


@app.route('/')
def home():
    return render_template('home_page.html', topics=grab_all_topics())

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''registers user ADD: and if username and password is not unique it prompts the user to enter a new one'''
    registered = True
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        if new_user.create_user():
            session['username'] = username
            return redirect('/user/' + username) #CREAT LOGIN/LOGOUT SESSION WITH USER LATER ON
        registered = False
    return render_template('registration_page.html', registered=registered)

@app.route('/user/<username>')
def username(username):
    '''shows user profile'''
    searched_for_account = {'username': username}
    searched_for_account = users_database.find_one(searched_for_account)
    date_joined = searched_for_account['datejoined']
    user_post = searched_for_account['posts_id']
    return render_template('user_page.html', username=username, datejoined=date_joined, user_post=user_post
                           , find_post=find_post)

@app.route('/topic/<topic_title>')
def topics(topic_title):
    '''shows posts for specific topic titles'''
    topic_title = topic_title.replace('%20',' ')
    return render_template('topic_page.html', topic=topic_title, posts=posts_database.find({'topic_title':topic_title})
                            ,find_author =find_author)


@app.route('/login', methods=['GET', 'POST'])
def login():
    invalid_creditals = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validate_username = users_database.find_one({'username': username},True)
        validate_password = users_database.find_one({'password': password},True)
        if validate_password is not None and validate_username is not None:
            session['username'] = username
            session['nickname'] = username
            return redirect('/user/' + username)
        invalid_creditals = True
    return render_template('login_page.html',invalid_creditals=invalid_creditals)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user = session['username']
        user = users_database.find_one({'username':user})
        post = Post(content,title,user['userID'])
        post.upload_post()
        user['posts_id'].append(post.post_id)
        users_database.update({'username':user['username']}, user)
        return redirect('/topic/' + title)
    return render_template('create_post_page.html')

@app.route('/delete/<post_id>')
def delete(post_id):
    delted_post = posts_database.find_one({'post_id':post_id})
    owner_of_post = users_database.find_one({'userID':delted_post['user_id']})
    posts_database.delete({'post_id': post_id})
    return redirect('/user/' + owner_of_post['username'])

def grab_all_topics():
    '''Grabs all the topic titles in the post Database'''
    topics = []
    for post in posts_database.show_all_entries():
        if 'topic_title' in post and 'text' in post and 'user_id' in post:
            if post['topic_title'] not in topics:
                topics.append(post['topic_title'])
    return topics

def find_author(id):
    '''takes post id and query's the database to find the author of the post'''
    author = users_database.find_one(id)
    return author['username']

def find_post(id):
    return posts_database.find_one({'post_id':id},verify_user=True)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
