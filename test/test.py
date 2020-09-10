#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest

class TestCalc(unittest.TestCase):
    "テストのテスト"

    def test_add(self):
        self.assertEqual(1 + 2, 3)

    def test_sub(self):
        self.assertEqual(2 - 1, 1)

if __name__ == "__main__":
    unittest.main()