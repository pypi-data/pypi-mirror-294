from setuptools import setup, find_packages

setup(
    name='bash_buddy_cli',
    version='0.1.2',
    packages=find_packages(where='src'),  # Specify the source directory
    package_dir={'': 'src'},  # Map the package root to the src directory
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
            'buddy=src.main:main',  # Adjust the entry point to include the src prefix
        ],
    },
)