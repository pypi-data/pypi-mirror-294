from setuptools import setup, find_packages

setup(
    name='lightweight_orchestration',
    version='0.1.0',
    description='Lightweight orchestration processes for intelligence jobs in Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Carlos Miranda Durand',
    author_email='carlosm@proactiveingredient.com',
    url='https://github.com/Proactive-Ingredient/lightweight_orchestration.git',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='AGPL-3.0-or-later',
)
