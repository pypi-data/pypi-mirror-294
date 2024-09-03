from pathlib import\
	Path
import re
import sys


_ENCODING_UTF8 = "utf-8"
_MODE_R = "r"
_MODE_W = "w"
_NEW_LINE = "\n"

_REGEX_IMPORT = "import .+"
_REGEX_FROM_IMPORT = "from .+ import .+"


def _append_to_sys_path(some_path):
	if some_path is not None:
		path_as_str = str(some_path)

		if path_as_str not in sys.path:
			sys.path.append(path_as_str)


def _ensure_is_path(obj):
	if isinstance(obj, Path):
		return obj

	elif isinstance(obj, str):
		return Path(obj)

	else:
		raise TypeError(
			"An argument of type string or pathlib.Path is expected.")


def _is_import_statement(some_str):
	if re.match(_REGEX_IMPORT, some_str) is not None:
		return True

	if re.match(_REGEX_FROM_IMPORT, some_str) is not None:
		return True

	return False


def read_reprs(file_path, importations=None, ignore_except=False):
	"""
	If a text file contains the representation of Python objects, this function
	can read it to recreate those objects. Each line must be a string returned
	by function repr. Empty lines are ignored.

	Recreating objects requires to import their class. For this purpose, you
	need to provide a dictionary mapping the appropriate import statements
	(keys, type str) to the path to the imported class (value, type str or
	pathlib.Path). However, if the imported class is from a built-in module or
	the standard library, set the value to None. Statements that are not
	importations will not be executed.

	Args:
		file_path (str or pathlib.Path): the path to a text file that contains
			object representations
		importations (dict): the import statements (keys, type str) and the
			paths to imported classes (values, type str or pathlib.Path)
			required to recreate the objects. Defaults to None.
		ignore_except (bool): If it is True, exceptions raised upon the parsing
			of object representations will be ignored. Defaults to False.

	Returns:
		list: the objects recreated from their representation

	Raises:
		ModuleNotFoundError: if argument importations contains a fault.
		Exception: any exception raised upon the parsing of an object
			representation if ignore_except is False.
	"""
	if importations is not None:
		for importation, path in importations.items():
			if _is_import_statement(importation):
				_append_to_sys_path(path)
				exec(importation)

	file_path = _ensure_is_path(file_path)

	with file_path.open(mode=_MODE_R, encoding=_ENCODING_UTF8) as file:
		text = file.read()

	raw_lines = text.split(_NEW_LINE)

	objs = list()

	for line in raw_lines:
		if len(line) >= 1:
			try:
				objs.append(eval(line))
			except Exception as e:
				if not ignore_except:
					raise e

	return objs


def write_reprs(file_path, objs):
	"""
	Writes the representation of Python objects in a text file. Each line is a
	string returned by function repr. If the file already exists, this function
	overwrites it.

	Args:
		file_path (str or pathlib.Path): the path to the text file that will
			contain the object representations
		objs (list, set or tuple): the objects whose representation will be
			written
	"""
	file_path = _ensure_is_path(file_path)

	with file_path.open(mode=_MODE_W, encoding=_ENCODING_UTF8) as file:
		for obj in objs:
			file.write(repr(obj) + _NEW_LINE)
