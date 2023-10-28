from setuptools import setup

setup(
    name='idync-api',
    description='An API to find available IDNYC appointments.',
    version='1.0',
    packages=['idnyc_api'],
    install_requires=[ 'httpx', 'fake-useragent'],
    author = 'Jacob Padilla',
    author_email = 'jp@jacobpadilla.com',
    url='https://jacobpadilla.com'
)