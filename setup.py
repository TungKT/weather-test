from setuptools import setup, find_packages
setup(
    name='weathertest',
    version='2.0.0',
    packages=find_packages(),
    py_modules=['runtest'],
    entry_points={
        'console_scripts': [
            'run-weather-test = runtest:main',
        ]
    },
    install_requires=[
        'pandas==1.3.5',
        'requests==2.28.2',
        'beautifulsoup4==4.9.3',
        'tabulate==0.9.0',
    ],
)