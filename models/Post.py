import uuid
from Database import Database

class Post(object):

    def __init__(self,text,topic_title,user_id):
        self.text = text
        self.topic_title = topic_title
        self.post_id = str(uuid.uuid4())
        self.user_id = user_id
        self.posts_database = Database('MessageBoard', 'posts', 'mongodb://127.0.0.1:27017')

    def json(self):
        return {
            'text': self.text,
            'topic_title': self.topic_title,
            'post_id': self.post_id,
            'user_id': self.user_id
        }

    def upload_post(self):
        self.posts_database.insert(self.json())

    def delete_post(self,post_id):
        '''post id show look like {'post_id': self.post_id}'''
        self.posts_database.delete(post_id)