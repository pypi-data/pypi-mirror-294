from setuptools import setup


def read_file():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(name='pypi-test-lib', version='1.0.0', description='This is a test lib.', packages=['sub_package'],
      py_modules=['pypi_test'], author='sz', author_email='xixihaha@qq.com',
      long_description=read_file(), license='MIT')
