from setuptools import setup

setup(
    name='NightPy',
    version='2018.1.1',

    description='NightBot API wrapper.',

    # The project's main homepage.
    url='https://www.IamGregAmato.com',

    # Author details.
    author='Greg Amato',
    author_email='amatobahn@gmail.com',

    # License
    license='Apache License v2.0',

    # Classifiers
    classifiers=[
        # Project Stage:
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    # Keywords
    keywords=['NightPy', 'NightBot', 'Amatobahn', 'API'],

    packages=['NightPy'],

    # Required dependencies. Will be installed by pip
    # when the project is installed.
    install_requires=['requests'],
)
