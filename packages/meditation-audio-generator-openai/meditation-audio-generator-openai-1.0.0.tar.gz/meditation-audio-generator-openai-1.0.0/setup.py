from setuptools import setup, find_packages

setup(
    name='meditation-audio-generator-openai',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pedalboard', 'pydub', 'openai', 'elevenlabs'
    ],
    author='Alexis Kirke',
    author_email='alexiskirke2@gmail.com',
    description='A tool to create guided audio meditations (like those found on YouTube but in audio-only form) using OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
