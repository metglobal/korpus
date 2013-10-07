from setuptools import setup

setup(
    name='korpus',
    version='0.0.1',
    description='similarity made easy!',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Metglobal',
    author_email='kadir.pekel@metglobal.com',
    url='https://github.com/metglobal/korpus',
	py_modules=['korpus'],
    tests_require=[
        'mock'
    ]
)
