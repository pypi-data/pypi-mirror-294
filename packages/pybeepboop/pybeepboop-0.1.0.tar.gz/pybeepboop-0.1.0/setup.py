import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "pybeepboop",
	version = "0.1.0",
	author = "Milk_Cool",
	author_email = "coder.tomsk@gmail.com",
	description = "A library in Python and C to create music in Python",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/Milk-Cool/pybeepboop",
	project_urls = {
		"Bug Tracker": "https://github.com/Milk-Cool/pybeepboop/issues",
	},
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir = {"": "src"},
	packages = setuptools.find_packages(where="src"),
	python_requires = ">=3.6"
)
