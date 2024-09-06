from setuptools import setup, find_packages

setup(
    name='vimal_tech_hello',
    version='0.1.0',
    author='Vimal P',
    description='A simple Hello World package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # Update with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
