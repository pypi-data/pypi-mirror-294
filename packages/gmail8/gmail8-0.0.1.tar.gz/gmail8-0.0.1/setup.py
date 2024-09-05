from setuptools import setup, find_packages

if __name__ == '__main__':
    version = '0.0.1'
    setup(
        name='gmail8',
        version=version,
        description = 'A decorator',
        long_description = 'Make your email powerful using python.',
        install_requires=[
            'requests',
        ],
        author='Junbin Gao',
        author_email='gao.junbin.cn@gmail.com',
        license='Apache License 2.0',
        packages=find_packages(),
        url='https://github.com/gaojunbin/gmail.git'
    )
