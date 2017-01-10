import uuid
from Database import Database
class Topic(object):

    def __init__(self,title,description,post_ids):
        self.title = title
        self.description = description
        self.topic_id = uuid.uuid4()
        self.post_ids = post_ids
        self.topics_database = Database('MessageBoard','topics','mongodb://127.0.0.1:27017')


    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'topic_id': self.topic_id,
            'post_ids': self.post_ids
        }


