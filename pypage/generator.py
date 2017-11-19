import os
import shutil
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from .reader import MarkdownReader
from .article import Article

_SINGLE_PAGE = ('base', )
_DEFAULT_CONTEXT = {
    'SITENAME': 'Juice',
    'OWNER': 'Mega Hertz',
    'HOME_URL': 'http://example.com',
    'THEME': 'default',
    'INPUT_PATH': 'content',
    'OUTPUT_PATH': 'output',
}

# Convert `path/filename.ext` to `filename`
get_filename = lambda x: os.path.splitext(x)[0].split(os.sep)[-1]
# Get the file extension name
get_fileext = lambda x: os.path.splitext(x)[-1]

class Generator(object):

    def __init__(self, **kwargs):
        self.context = _DEFAULT_CONTEXT.copy()
        self.context.update(kwargs)

    def get_files(self, path):
        files = []
        for root, dirs, temp_files in os.walk(path, followlinks=True):
            files.extend([os.path.join(root, file) for file in temp_files])
        return files

    def get_templates(self, path):
        env = Environment(loader=FileSystemLoader(path))

        templates = {}
        for template in ('article', ):
            try:
                templates[template] = env.get_template('%s.html' % template)
            except TemplateNotFound:
                raise Exception("Unable to load {}.html from {}".format(template, path))

        return templates

    def generate_file(self, filename, template, context, **kwargs):

        context = context.copy()
        context.update(kwargs)
        output = template.render(context)
        filename = os.path.join(self.context['OUTPUT_PATH'], filename)

        # Remove all existing files from output folder
        try:
            shutil.rmtree(self.context['OUTPUT_PATH'])
        except:
            pass
        os.mkdir(self.context['OUTPUT_PATH'])

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)


class ArticleGenerator(Generator):

    def __init__(self, **kwargs):
        super(ArticleGenerator, self).__init__(**kwargs)
        self.articles = []

    def process_files(self, files):
        reader = MarkdownReader()
        for f in files:
            content, metadatas = reader.read(f)
            article = Article(get_filename(f), content, metadatas)

            # TODO Check content is valid

            self.articles.append(article)

    def generate(self):
        templates = self.get_templates(os.path.join(
            'themes', self.context['THEME']
        ))

        files = self.get_files(self.context['INPUT_PATH'])
        self.process_files(files)

        for article in self.articles:
            self.generate_file(article.name + '.html',
                               templates['article'],
                               self.context,
                               article=article)
