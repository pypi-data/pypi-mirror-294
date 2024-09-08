from setuptools import setup, find_packages

setup(
    name='uzweb',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # kerakli kutubxonalar ro‘yxati
    ],
    entry_points={
        'console_scripts': [
            'uzweb = uzweb.cli:main',  # Terminal buyruqlari uchun
        ],
    },
    author='Sizning Ismingiz',
    author_email='your.email@example.com',
    description='no description',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
