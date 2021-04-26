import os
import unittest
from unittest import mock
from unittest.mock import patch
from hashapp.fileHashChecker import text_to_data_dict, check_files_hashes, compare_strings, print_results, get_hash, get_target_file_content


param_list_for_compare_strings = [
    ["compare same strings", "b2juif4", "b2juif4", "OK"],
    ["compare same strings (nums)", "8888", "8888", "OK"],
    ["compare string and num", "8888", 8888, "FAIL"],
    ["compare not same strings", "b2juif4", "b2juif", "FAIL"],
    ["compare same nums", 34, 34, "FAIL"],
]

param_list_for_get_hash = [
    ["norm md5", "i love pizza", "md5", True, "ae6749310a949f8f250c38519ea5527a",],
    ["norm sha1", "i love pizza", "sha1", True, "879de7dfce0dc836071e5ac06bbf053a07c18e61",],
    ["norm sha256", "i love pizza", "sha256", True, "391b62fa80ca018cbcb90967fc65c1dbb5bcc05f5207e064a4d5d2bd810eb746",],
    ["alg doesn't exist", "i love pizza", "sha2567", False, 'NOT FOUND',],
]


class TestFileHashChecker(unittest.TestCase):

    def test_compare_strings(self):
        """Test that it can compare strings."""

        for test_name, val1, val2, exp_result in param_list_for_compare_strings:
            with self.subTest(name=test_name):
                actual_result = compare_strings(val1, val2)
                self.assertEqual(actual_result, exp_result)


    def test_get_target_file_content(self):
        """Test that it can get file content."""

        test_filename = "testFile.txt"
        test_str = "This is a test!"

        with open(test_filename, "w") as tf:
            tf.write(test_str)

        dirpath = os.path.abspath(os.getcwd())
        filepath = os.path.join(dirpath, test_filename)
        
        actual_isfile, actual_result = get_target_file_content(filepath)
        exp_isfile, exp_result = True, test_str
        self.assertEqual(actual_isfile, exp_isfile)
        self.assertEqual(actual_result, exp_result)

        os.remove(test_filename)

        actual_isfile, actual_result = get_target_file_content(filepath)
        exp_isfile, exp_result = False, 'NOT FOUND'
        self.assertEqual(actual_isfile, exp_isfile)
        self.assertEqual(actual_result, exp_result)


    def test_get_hash(self):
        """Test that it can check content hash."""

        for test_name, test_content, test_hash_alg, exp_ok, exp_result in param_list_for_get_hash:
            with self.subTest(name=test_name):
                actual_ok, actual_result = get_hash(test_content, test_hash_alg)
                self.assertEqual(actual_ok, exp_ok)
                self.assertEqual(actual_result, exp_result)


    @mock.patch('hashapp.fileHashChecker.get_target_file_content')
    @mock.patch('hashapp.fileHashChecker.get_hash')
    @mock.patch('hashapp.fileHashChecker.compare_strings')
    def test_check_files_hashes(self, mock_compare_strings, mock_get_hash, mock_get_target_file_content):
        """Test that it can check all target files hashes."""

        test_path_to_dir = "any path"
        test_target_files_props_dict = {"filename": ["file1.txt"], "hash_alg": ["any_alg"], "hash_str": ["any_str"]}

        mock_get_target_file_content.return_value = False, "NOT FOUND"

        exp_result = [["file1.txt", "NOT FOUND"]]
        actual_results = check_files_hashes(test_path_to_dir, test_target_files_props_dict)
        self.assertEqual(actual_results, exp_result)

        mock_get_target_file_content.return_value = True, "hello"
        mock_get_hash.return_value = False, "NOT FOUND"
        actual_results = check_files_hashes(test_path_to_dir, test_target_files_props_dict)
        self.assertEqual(actual_results, exp_result)

        exp_result = [["file1.txt", "OK"]]
        mock_get_hash.return_value = True, "hello_hash"
        mock_compare_strings.return_value = "OK"
        actual_results = check_files_hashes(test_path_to_dir, test_target_files_props_dict)
        self.assertEqual(actual_results, exp_result)

        exp_result = [["file1.txt", "FAIL"]]
        mock_compare_strings.return_value = "FAIL"
        actual_results = check_files_hashes(test_path_to_dir, test_target_files_props_dict)
        self.assertEqual(actual_results, exp_result)      


    def test_text_to_data_dict(self):
        """Test that it can transform text to dictionary with data."""

        actual = text_to_data_dict("1 2 3\n4 5 6\n")
        expected = {"filename": ["1", "4"], "hash_alg": ["2", "5"], "hash_str": ["3", "6"]}
        self.assertEqual(actual, expected)

        actual = text_to_data_dict("1 2 3\n4 5 6\n7 8 9\n")
        expected = {"filename": ["1", "4", "7"], "hash_alg": ["2", "5", "8"], "hash_str": ["3", "6", "9"]}
        self.assertEqual(actual, expected)


    @mock.patch('hashapp.fileHashChecker.print')
    def test_print_results(self, mock_print):
        """Test that it can print results."""

        mock_print.return_value = None
        results_arr = [["f1.txt", "OK"], ["f2.bin", "FAIL"], ["f3.txt", "NOT FOUND"]]
        print_results(results_arr)
        
        self.assertEqual(mock_print.call_count, len(results_arr))


if __name__ == '__main__':
    unittest.main()
