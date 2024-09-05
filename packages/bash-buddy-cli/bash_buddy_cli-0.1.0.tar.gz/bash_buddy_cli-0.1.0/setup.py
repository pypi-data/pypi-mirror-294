from setuptools import setup, find_packages

setup(
    name='bash_buddy_cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv==1.0.1',
        'openai==1.43.0'
    ],
    extras_require={
        'dev': [
            'setuptools==74.1.1',
            'wheel==0.44.0',
            'twine==5.1.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'buddy=src.main:main',
        ],
    },
)