import datetime
import uuid
from Database import Database
from models.Post import Post

class User(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.userID = str(uuid.uuid4())
        self.dateJoined = str(datetime.datetime.utcnow())
        self.post_ids = list()
        self.users_database = Database('MessageBoard','users','mongodb://127.0.0.1:27017')


    def json(self):
        '''json/info for the user which is placed into the database'''
        return {
            'username': self.username,
            'password':self.password,
            'datejoined': self.dateJoined,
            'userID': self.userID,
            'posts_id': self.post_ids
        }

    def create_post(self,subject,text,topic_title):
        '''creates a post'''
        post = Post(subject,text,topic_title,self.userID)
        post.upload_post()
        self.post_ids.append(post.post_id)
        self.users_database.update({'userID': self.userID}, self.json())

    def delete_post(self,post_id):
        '''delete a user post\'s by the post\s and return true if the post was deleted'''
        if post_id in self.post_ids:
            self.post_ids.remove(post_id)
            self.users_database.update({'userID': self.userID}, self.json())
            return True
        return False

    def create_user(self):
        '''creates a new user and returns true if the user was created'''
        if self.unique_creditals():
            self.users_database.insert(self.json())
            return True
        return False

    def unique_creditals(self):
        '''returns true if the username and password does not exist in the database'''
        if (self.users_database.find_one({'username': self.username}) == None and
                    self.users_database.find_one({'password': self.password}) == None):
            return True
        return False
