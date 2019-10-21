# coding=utf-8
"""Install config."""
from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name='voxpopuli',
    version='0.3.3',
    description='A wrapper around Espeak and Mbrola, to do simple Text-To-Speech (TTS),'
                ' with the possibility to tweak the phonemic form.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hadware/voxpopuli',
    author='Hadware',
    author_email='hadwarez@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tts speech phonemes audio',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'])
