from setuptools import setup, find_packages

setup(
    name='ja_ai_module',
    version='0.0.2',
    description='PYPI tutorial package creation written by Jerry',
    author='Jerry',
    author_email='m9511003@gmail.com',
    url='https://github.com/jerry/ja_ai',
    install_requires=['tqdm', 'pandas', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['jaen', 'ja', 'python datasets', 'python tutorial', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)