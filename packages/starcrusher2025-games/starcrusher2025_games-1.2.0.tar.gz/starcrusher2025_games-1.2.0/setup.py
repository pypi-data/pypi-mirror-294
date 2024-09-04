from setuptools import setup, find_packages

setup(
    name='starcrusher2025_games',
    version='1.2.0',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'starcrusher2025-games = starcrusher2025_games.game:main',
        ],
    },
    author='starcrusher2025',
    description='A easy to use game engine.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/starcrusher2025/2025_games',
    license='MIT',
)
#python setup.py sdist bdist_wheel
#twine upload dist/*