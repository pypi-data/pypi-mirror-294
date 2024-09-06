from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.3')
print('     setup: module :  falcon_logger')

# @formatter:off
setup(
    description='module for faster python logging',
    # TODO update as needed
    keywords=['gui', 'test', 'verification'],
    install_requires=[
        'medver-pytest',
        'pytest',
        # TODO update as needed
        # 'socket-oneline',
    ],
    classifiers=[
        # TODO update as needed
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='falcon-logger',
    packages=find_packages(include='./falcon_logger*', ),
    include_package_data=True,
    exclude_package_data={'./falcon_logger/lib': ['.gitignore']},
    version='0.0.3',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='J. Arrizza',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/falcon-logger/src/master',
    download_url='https://bitbucket.org/arrizza-public/falcon-logger/get/master.zip',
)
# @formatter:on

print('     setup: done')
