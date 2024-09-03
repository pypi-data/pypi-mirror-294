from setuptools import setup, find_packages
import os

long_description = ""
if os.path.exists('README.md'):
        with open('README.md', encoding='utf-8') as f:
            long_description = f.read()

setup(
    name='improved_helloworld',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'weatherwolf=weatherwolf.__main__:main'
        ]
    },
    author='WeatherWolf',
    author_email='golfbekkers@gmail.com',
    description='WeatherWolf is an extension on python to speed up your coding journey by skipping the first basic lesson',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/weatherwolf/Improved-HelloWorld',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
