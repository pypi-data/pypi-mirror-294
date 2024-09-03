import setuptools


def _make_long_description():
	with open("README.md", "r", encoding="utf-8") as readme_file:
		readme_content = readme_file.read()

	fr_index = readme_content.index("## FRANÇAIS")
	fr_demos_index = readme_content.index("### Démos")
	en_index = readme_content.index("## ENGLISH")
	en_demos_index = readme_content.index("### Demos")

	return readme_content[fr_index:fr_demos_index]\
		+ readme_content[en_index:en_demos_index].rstrip()


if __name__ == "__main__":
	setuptools.setup(
		name = "repr_rw",
		version = "1.0.1",
		author = "Guyllaume Rousseau",
		description = "This library writes Python object representations in a text file and reads the file to recreate the objects. An object representation is a string returned by function repr.",
		long_description = _make_long_description(),
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/repr_rw",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		packages = setuptools.find_packages(exclude=("demos", "demo_package",)),
		license = "MIT",
		license_files = ("LICENSE",))
