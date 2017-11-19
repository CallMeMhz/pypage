from setuptools import setup

setup(
    name='pypage',
    version='1.0',
    description='Generate static html pages from text marked up',
    license='MIT',
    author='Mega Hertz',
    author_email='callmemhz@gmail.com',
    url='callmemhz.github.io',
    packages=['pypage'],
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
