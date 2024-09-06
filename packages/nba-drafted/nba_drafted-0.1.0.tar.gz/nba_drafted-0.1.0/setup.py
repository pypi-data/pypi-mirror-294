from setuptools import setup, find_packages

setup(
    name='nba_drafted',  
    version='0.1.0',
    description='A package for NBA dataset preparation, feature engineering, training model and predicting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ShivamArora99/NBA_drafted_package',  # Update with your GitHub repo
    author='Shivam Arora',
    author_email='saror.off@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'plotly',
        'category_encoders'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
