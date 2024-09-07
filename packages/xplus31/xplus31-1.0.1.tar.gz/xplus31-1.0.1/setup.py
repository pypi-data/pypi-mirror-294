from setuptools import setup, find_packages
from pkg_resources import parse_requirements
NAME = 'xplus31'
with open( '%s/README.md'%NAME, encoding = 'utf-8' ) as fp:
    long_description = fp.read()
with open( 'requirements.txt', encoding = 'utf-8' ) as fp:
    install_requires = list(map(str,parse_requirements(fp)))
setup(
    name = NAME,
    version = '1.0.1',
    description = '''
        A simple test of package distribution with simple functions in it
    ''',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'A.T.P.test',
    author_email = 'nonsense@fake.email',
    url = 'https://pypi.org/project/%s'%NAME,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Education',
        'License :: Freeware',
        'Operating System :: Microsoft :: Windows'    
    ],
    install_requires = install_requires,
    packages = find_packages(),
    include_package_data = True,
    package_data = { 'xplus31': ['README.md'] },
    entry_points = { 'console_scripts': ['31_help = src:help'] }
)
