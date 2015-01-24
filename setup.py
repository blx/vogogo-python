from distutils.core import setup

setup(
    name='vogogo',
    version='0.1',
    packages=['vogogo'],
    url='https://github.com/LawnmowerIO/vogogo-python',
    license='MIT',
    author='Pieter Gorsira',
    package_data={'README': ['README.md']},
    author_email='pgorsira@gmail.com',
    description='Python bindings for Vogogo API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='api, client, vogogo',
    install_requires=[
        'httplib2>=0.8',
        'requests>=1.1.0',
        'oauth2client>=1.1',
        'python-dateutil>=2.2',
        'enum34==1.0',
    ],
    tests_require=[
        'sure>=1.2.5',
        'httpretty>=0.8.0',
        'mock',
    ],
)
