from setuptools import setup, find_packages

setup(
    name='flaskmotion',
    version='0.1.8',
    description='A Flask package for smooth page transitions using AJAX and CSS fade effects.',
    author='Daniël Beukes',
    author_email='your_email@example.com',
    url='https://github.com/beukzdev/flaskmotion',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=1.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
