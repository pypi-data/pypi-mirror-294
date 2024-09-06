from setuptools import find_packages, setup

setup(
    name='lor_gdp_tools',
    packages=find_packages(),
    version='0.1.2',
    description='This is a utility package designed to enable data scientitists and analysts to easily access GDP data within a python environment',
    author="Damian Rumble <DRumble@laingorourke.com>"
)

### Python code to publish package ###
#python setup.py sdist bdist_wheel
#twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDZiMTc4ODU4LWIwYzYtNDZhNC04M2RjLWFmYzk0MTViYmJlMQACKlszLCIyOGMzOGI0OS01YTRhLTQxNzEtYTMzNy0xMWU2MGVlYzBiNTkiXQAABiAwGpNFLruzLptgrJ8R0-EmmYp6SfGLNSK2DfyOy0y7gA dist/*