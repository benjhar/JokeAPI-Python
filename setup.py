import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name='jokeapi',
  packages=['jokeapi'],
  version='0.1.3',
  license='GNU General Public License v3 (GPLv3)',
  description='An API Wrapper for Sv443\'s JokeAPI',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='thenamesweretakenalready',
  author_email='leet_haker@cyber-wizard.com',
  url="""https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper""",
  download_url='https://github.com/user/Sv443s-JokeAPI-Python-Wrapper/archive/v0.1.3.tar.gz',
  keywords=['api wrapper', 'wrapper', 'api', 'jokes'],
  install_requires=setuptools.find_packages(),
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.8',
  ],
)
