from unittest.mock import patch
import unittest

import src.database as db
import res.globals as glb
import src.main as mn

import builtins


# Çıktı ekrana yazdırılmasın diye
def print_foo(*args, **kwargs): pass
builtins.print = print_foo


class Tester(unittest.TestCase):
	def test_test(self):
		self.assertEqual(1, 1)
	
	@patch("src.main.get_input", return_value="ls")
	def test_ls(self, *args, **kwargs):
		*_, main_rv = mn._main(loop=False)
		self.assertEqual(main_rv, True)
		
	@patch("src.main.get_input", return_value="ls tyt")
	def test_ls_f(self, *args, **kwargs):
		*_, main_rv = mn._main(loop=False)
		self.assertEqual(main_rv, True)

	@patch("src.main.get_input", return_value="ls /tyt")
	def test_ls_rf(self, *args, **kwargs):
		*_, main_rv = mn._main(loop=False)
		self.assertEqual(main_rv, True)

	@patch("src.main.get_input", return_value="ls tyt/sos/")
	def test_ls_fs(self, *args, **kwargs):
		*_, main_rv = mn._main(loop=False)
		self.assertEqual(main_rv, True)

	@patch("src.main.get_input", return_value="ls /tyt/sos/")
	def test_ls_rfs(self, *args, **kwargs):
		*_, main_rv = mn._main(loop=False)
		self.assertEqual(main_rv, True)

if __name__ == "__main__":
	unittest.main()
