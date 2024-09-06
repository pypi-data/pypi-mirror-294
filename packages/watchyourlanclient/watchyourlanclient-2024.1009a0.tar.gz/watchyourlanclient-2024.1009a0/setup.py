from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='watchyourlanclient',
    version="2024.1009-alpha",
    description='Python client to talk to WatchYourLAN APIs',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='David Wahlstrom',
    author_email='david.wahlstrom@gmail.com',
    url='https://github.com/drwahl/py-watchyourlanclient',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    # package_data={'watchyourlanclient': ['templates/*']},
    include_package_data=True,
    install_requires=[
        'bumpver',
        'cachetools>=5.5.0',
        'httpx>=0.27.0',
    ],
)
