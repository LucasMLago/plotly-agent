from setuptools import setup, find_packages

setup(
    name='plotly-agent',
    version='0.1.1',
    license='MIT License',
    packages=find_packages(),
    install_requires=[
        'langchain>=0.2.11',
        'plotly>=5.23.0',
        'pandas>=2.2.2',
        'nbformat>=5.10.4'
    ],
    author='Lucas Lago',
    author_email='lukemartinslagonit@gmail.com',
    keywords='plotly agent',
    description='Visualize your data with langchain and plotly as a plotly agent',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LucasMLago/plotly-agent',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)