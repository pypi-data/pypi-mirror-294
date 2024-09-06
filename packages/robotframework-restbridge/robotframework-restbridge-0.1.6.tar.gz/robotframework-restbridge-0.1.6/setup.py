# setup.py
from setuptools import setup
from os.path import abspath, dirname, join


VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', 'RestBridgeLibrary', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

setup(
    name='robotframework-restbridge',
    version=VERSION,
    package_dir={'': 'src'},
    packages=['RestBridgeLibrary'],
    install_requires=[
        'robotframework',
        'flask',
        'robotframework-browser',
        'robotframework-requests',
        'jsonpickle',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='Your Name',
    author_email='PyPI.Releases@viadee.de',
    description='This is a robotframework keyword library to allow single command execution via HTTP.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/raffelino/robotframework-restbridge',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
