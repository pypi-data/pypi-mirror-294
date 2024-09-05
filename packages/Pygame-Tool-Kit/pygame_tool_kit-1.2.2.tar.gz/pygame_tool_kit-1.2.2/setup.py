from setuptools import setup, find_packages

setup (
	name = "Pygame_Tool_Kit",
	version = "1.2.2",
	author = "Gloacking",
	description = "Un conjunto de herramientas útiles para el desarrollo de videojuegos con Pygame.",
	long_description = open ("README.md").read (),
	long_description_content_type="text/markdown",
	url = "https://github.com/gloacking/Pygame_Tool_Kit",
	packages = find_packages (exclude = ["env*"]),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires = ">=3.10",
	install_requires = [
		"pygame"
	],
	include_package_data = True
)
