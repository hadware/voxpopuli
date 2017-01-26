# coding=utf-8
"""Install config."""
from setuptools import setup, find_packages

setup(
    name='voxpopuli',
    version='0.1',
    description='A wrapper around Espeak and Mbrola, to do simple Text-To-Speech (TTS),'
                ' with the possibility to tweak the phonemic form.',
    url='https://github.com/hadware/voxpopuli',
    author='Hadrien Titeux',
    author_email='carlthome@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Speech'
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='tts speech phonems audio',
    packages=find_packages(),
    install_requires=['pyaudio'],
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['nose'])
