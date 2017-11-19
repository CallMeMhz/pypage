from datetime import datetime

_datetime_format = '%Y-%m-%d %H:%M'
_format_time = lambda x: datetime.strptime(x, _datetime_format)

class Article(object):

    def __init__(self, name, content, metadatas):
        self.name = name
        self.content = content
        self.title = metadatas['title']
        self.author = metadatas['author']
        self.created_at = _format_time(metadatas['created_at'])
        if 'modified_at' in metadatas:
            self.modified_at = _format_time(metadatas['modified_at'])
        if 'tags' in metadatas:
            self.tags = metadatas['tags'].split(', ')
