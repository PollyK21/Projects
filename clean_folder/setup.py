from setuptools import setup

setup(
    name='clean_folder',
    version='1',
    description='clean folder',
    url='https://github.com/PollyK21/Projects',
    author='Polina Kulish',
    author_email='pol.kulish@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)