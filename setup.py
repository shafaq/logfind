try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Application to list files which contain search word',
    'author': 'Shafaq',
    'url': 'www.shafaqmaalik.com',
    'download_url': 'Where to download it.',
    'author_email': 'shafaq.maalik@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['logfind'],
    'scripts': [],
    'name': 'logfind'
}
