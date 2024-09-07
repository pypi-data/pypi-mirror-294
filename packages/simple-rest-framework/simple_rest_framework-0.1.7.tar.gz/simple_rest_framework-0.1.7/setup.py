from setuptools import setup

setup(
    name='simple_rest_framework',
    version='0.1.7',
    packages=['simple_rest_framework'],
    install_requires=[
        'djangorestframework',
    ],
    author='Valentin Cabrera',
    author_email='valentincabrera2003@gmail.com',
    description='Esta libreria permite agilizar el desarrollo de APIs REST en Django. Manejando un CRUD básico de forma automática y manejando excepciones de forma sencilla.',
    url='https://github.com/ValentinCabrera/simple_rest_framework',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)