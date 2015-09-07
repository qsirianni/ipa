#!/usr/bin/python

"""
Contains unit tests for the IPA script

Author: Quinton Sirianni
"""

import os
import os.path
import unittest
from subprocess import CalledProcessError
from unittest import TestCase

import ipa


class TestCheckEnv(TestCase):
    """Tests involving check_env()"""

    def setUp(self):
        """Setup code for the tests"""

        # Operating system name needs to be recorded from os module
        self._os_name = os.name

    def tearDown(self):
        """Tear down code for tests"""

        # Operating system type needs to be restored to os module
        os.name = self._os_name

    def test_utils_exist(self):
        """Should not raise an exception when checking for the echo utility"""

        try:
            os.name = 'posix'
            ipa.check_env(['echo'])

        except CalledProcessError:
            self.fail('check_env() raised a CalledProcessError unexpectedly')

    def test_utils_absent(self):
        """Should raise an exception when checking for a non-existent utility"""

        os.name = 'posix'

        with self.assertRaises(CalledProcessError):
            ipa.check_env(['this_utility_does_not_exist'])

    def test_utils_none(self):
        """Should raise an exception when given None as the required utilities"""

        with self.assertRaises(TypeError):
            ipa.check_env(None)

    def test_utils_empty(self):
        "Should not raise an exception when given an empty list of required utilities"

        try:
            ipa.check_env([])

        except CalledProcessError:
            self.fail('check_env() raised a CalledProcessError unexpectedly')

    def test_env_is_valid(self):
        """Should not raise an exception when environment is approved"""

        try:
            os.name = 'posix'
            ipa.check_env(['echo'])

        except OSError:
            self.fail('check_env() raised an OSError unexpectedly')

    def test_env_is_bad(self):
        """Should raise an exception when environment is not approved"""

        os.name = 'bad_env'
        with self.assertRaises(OSError):
            ipa.check_env(['echo'])


class TestBamToFq(TestCase):
    """Tests involving bam_to_fq()"""

    def setUp(self):
        """Setup code for tests"""

        # Available test file
        self._test_file = os.path.join('test_files', 'lambda_iontorrent.bam')

    def test_valid_file(self):
        """Should not raise an exception when a valid bam file is used"""

        try:
            ipa.bam_to_fq(self._test_file)

        except CalledProcessError:
            self.fail('bam_to_fq() raised a CalledProcessError unexpectedly')

    def test_absent_file(self):
        """Should raise an exception when the file does not exist"""

        with self.assertRaises(CalledProcessError):
            ipa.bam_to_fq('this_file_does_not_exist.bam')

    def test_no_file(self):
        """Should raise an exception when no file is given"""

        with self.assertRaises(ValueError):
            ipa.bam_to_fq('')

    def test_none_file(self):
        """Should raise an exception when None is given"""

        with self.assertRaises(AttributeError):
            ipa.bam_to_fq(None)

    def test_wrong_format(self):
        """Should raise an exception when the wrong type of file is used"""

        with self.assertRaises(ValueError):
            ipa.bam_to_fq("this_file_has_the_wrong_format.fq")


class TestReadCorrection(TestCase):
    """Tests involving read_correction()"""

    def setUp(self):
        """Setup code before tests"""

        # Available test file
        self._test_file = os.path.join('test_files', 'lambda_reads.fq')

    def test_valid_file(self):
        """Should not raise an exception when a valid FASTQ file is used"""

        try:
            ipa.read_correction(self._test_file)

        except CalledProcessError:
            self.fail('read_correction() raised a CalledProcessError unexpectedly')


if __name__ == '__main__':
    unittest.main()
