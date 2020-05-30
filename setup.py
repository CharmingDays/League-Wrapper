from setuptools import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()



setup(name='LeagueClient',
      author='Cheng Yue',
      url='https://github.com/Rapptz/discord.py',
      version="0.1",
      packages=['LeagueClient','api'],
      license='MIT',
      description='A Python wrapper for the League of Legends API',
      install_requires=requirements,
      python_requires='>=3.8.1',
)