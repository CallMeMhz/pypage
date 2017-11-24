from setuptools import setup
import os

setup(
    name='pypage',
    version='1.0',
    description='Generate static html pages from text marked up',
    license='MIT',
    author='Mega Hertz',
    author_email='callmemhz@gmail.com',
    url='callmemhz.github.io',
    packages=['pypage'],
    package_data={
        'pypage':[os.path.relpath(os.path.join(root, name), 'pypage')
                  for root, _, names in os.walk(os.path.join('pypage', 'themes'))
                  for name in names]},
    install_requires=[
        'jinja2',
        'markdown'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
    keywords='static github pages markdown blog',
    entry_points={
        'console_scripts': [
            'pypage = pypage.main:main'
        ]
    }
)
