from setuptools import setup, find_packages
setup(name='sing_app',
      version='0.1',
      description='Singing Instruction Portal and Database',
      url='localhost:5000',
      author='Edward Prah',
      author_email='eprahcareer@gmail.com',
      license='',
      packages=find_packages(include=['sing_app', 'sing_app.*']),
      zip_safe=False)