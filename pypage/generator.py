import os
import shutil
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from .reader import MarkdownReader
from .article import Article

_DEFAULT_CONTEXT = {
    'lang': 'zh',
    'site_name': 'Pypage',
    'site_desc': """Welcome to my website !""",
    'author': 'Mega Hertz',
    'prefix_url': 'http://example.com',
    'theme': 'default',
    'input_path': 'content',
    'output_path': 'output',
}
_THEMES_DIR = os.path.dirname(os.path.abspath(__file__))

# Convert `path/filename.ext` to `filename`
get_filename = lambda x: os.path.splitext(x)[0].split(os.sep)[-1]
# Get the file extension name
get_fileext = lambda x: os.path.splitext(x)[-1]


def remove_directory(path):
    try:
        shutil.rmtree(path)
    except:
        pass
    os.mkdir(path)


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
        for template in ('article', 'index'):
            try:
                templates[template] = env.get_template('%s.html' % template)
            except TemplateNotFound:
                raise Exception("Unable to load {}.html from {}".format(template, path))

        return templates

    def generate_file(self, filename, template, context, **kwargs):

        context = context.copy()
        context.update(kwargs)
        output = template.render(context)
        filename = os.path.join(self.context['output_path'], filename)

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
            _THEMES_DIR, 'themes', self.context['theme']
        ))

        files = self.get_files(self.context['input_path'])
        self.process_files(files)

        # Clean output path and copy theme to output directory
        remove_directory(self.context['output_path'])
        shutil.copytree(os.path.join(_THEMES_DIR, 'themes', self.context['theme'], 'css'),
                        os.path.join(self.context['output_path'], 'css'))

        # Generate home page
        self.generate_file('index.html',
                           templates['index'],
                           self.context,
                           articles=self.articles)

        # Generate articles pages
        for article in self.articles:
            self.generate_file(article.name + '.html',
                               templates['article'],
                               self.context,
                               article=article)
