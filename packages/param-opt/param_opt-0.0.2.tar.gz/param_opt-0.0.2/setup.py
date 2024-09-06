from setuptools import setup, find_packages

setup(
    name='param-opt',  # Replace with your own package name
    version='0.0.2',
    description='This repository features an ML approach toward estimating process parameters for production steps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/j-ehrhardt/p-opt',  # Replace with your package's URL
    author='Jonas Ehrhardt',
    # author_email='your.email@example.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',  # Specify the versions of Python your package supports
    ],
    packages=find_packages(),
    # install_requires=[ #list of dependencies
    #    ''
    # ],
    python_requires='>= 3.12',  # Python version requirements
)