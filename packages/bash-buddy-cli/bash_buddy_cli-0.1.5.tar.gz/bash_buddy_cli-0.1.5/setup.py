from setuptools import setup, find_packages

setup(
    name='bash_buddy_cli',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
        'openai==1.43.0'
    ],
    extras_require={
        'dev': [
            'setuptools==74.1.1',
            'wheel==0.44.0',
            'twine==5.1.1'
        ],
    },
    entry_points={
        'console_scripts': [
            'buddy=src.main:main',
        ],
    },
    author='TheRealJamesRussell',
    author_email='nope@example.com',
    description='A CLI tool for interacting with Meta Ads API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TheRealJamesRussell/BashBuddy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)