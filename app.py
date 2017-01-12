from Database import Database
from flask import redirect
from flask import request
from flask import Flask
from flask import render_template
from models.User import User
from models.Post import Post
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static')
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
    print(id)
    author = users_database.find_one(id)
    print(author)
    return author['username']

def find_post(id):
    return posts_database.find_one({'post_id':id})

def load_post():
    user = User("imnew19", 'new19')
    user.create_user()
    user.create_post('testing if post comes to user page2','testing if post goes to user19')

if __name__ == '__main__':
    load_post()
    app.run()
