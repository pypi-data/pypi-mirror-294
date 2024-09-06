from setuptools import setup, find_packages


setup(
    name='gpt-explorer',
    version='0.2.0',
    description='A package for gather the online data using GPT.',
    author='Worawut Boonpeang',
    author_email='zz.enlighten.zz@gmail.com',
    packages=find_packages(),  # Discovers packages from directory structure
    package_data={'gpt_explorer': ['*.pyc']},  # Include compiled bytecode files
    install_requires=[
        "requests>=2.28.1",
        "beautifulsoup4>=4.11.1",
        "googlesearch-python>=1.2.5",
        "openai>=0.28.1"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
