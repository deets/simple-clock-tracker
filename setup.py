from setuptools import setup, find_packages

setup(
    name='clocktracker',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clock-tracker=clocktracker.main:main'
        ]
    }
)
