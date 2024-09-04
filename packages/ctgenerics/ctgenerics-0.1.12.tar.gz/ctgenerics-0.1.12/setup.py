from setuptools import setup, find_packages

setup(
    name='ctgenerics',
    version='0.1.12',
    packages=find_packages(),
    description='A utility package for my STST projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Callum Thickett',
    author_email='callum.thickett@stepstone.com',
    url='https://github.com/thickett/ctgenerics',
    include_package_data=True,
    package_data={
        'ctgenerics':['config/sample_config.ini']
    },
    install_requires=[
        'SQLAlchemy~=1.4.25',
        'psycopg2-binary==2.9.9',
        'pandas~=2.2.2',
        'pydantic',
        'pyyaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'setup-project = ctgenerics.project_setup:main'
        ]
    }
)
