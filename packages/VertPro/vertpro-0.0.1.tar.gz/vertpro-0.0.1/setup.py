from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='VertPro',
    version='0.0.1',
    description='A tool made to aid with conversion in Python',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Umer Imran',
    author_email='um3rimran@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='convert',
    packages=find_packages(),
    install_requires=[]
)