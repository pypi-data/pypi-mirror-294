from setuptools import setup, find_packages

setup(
    name='FlaskMotion',
    version='0.1.6',
    description='A simple Flask extension for smooth page transitions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/beukzdev/FlaskMotion',  # Your repository URL
    author='Daniël Beukes',
    author_email='beukzgroup@outlook.com',
    license='MIT',
    packages=find_packages(),  # Automatically includes the flaskmotion package
    include_package_data=True,  # Includes files specified in MANIFEST.in
    install_requires=['Flask'],  # Flask is the only dependency
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
