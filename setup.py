from setuptools import setup, find_packages

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
    install_requires=['requests==2.2.1'],
    zip_safe=False,
    include_package_data=True,
)