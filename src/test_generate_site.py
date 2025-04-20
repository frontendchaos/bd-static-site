import unittest
import os

from generate_site import generate_page
from fileio import get_root_path


class TestGenerateSite(unittest.TestCase):
    def test_generate_site(self):
        # Define the paths for the test
        root = get_root_path()
        from_path = "test_from_path"
        template_path = root + "/template.html"
        dest_path = "test_dest_path"

        # Call the function to test
        retval = generate_page(from_path, template_path, dest_path)

        # Check if the destination path was created (you can add more checks as needed)
        first_line = "<!doctype html>"
        self.assertTrue(retval.startswith(first_line))