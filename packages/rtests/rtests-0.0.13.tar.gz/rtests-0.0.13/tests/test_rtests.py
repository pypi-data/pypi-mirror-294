import os
os.environ['R_HOME'] = r'C:\Program Files\R\R-4.3.1'

import unittest
import rtests



class TestRTests(unittest.TestCase):
    def test_regex_match2(self):
        a = [6.0, 4.0, 5.0, 5.0, 7.0, 6.0, 6.0, 6.0, 7.0, 6.0, 6.0, 5.0, 6.0, 6.0, 5.0, 5.0, 3.0, 6.0, 6.0, 5.0, 6.0, 5.0, 4.0, 6.0, 6.0, 6.0, 7.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 6.0, 4.0, 6.0, 6.0, 5.0, 7.0, 6.0, 6.0, 5.0, 6.0, 7.0, 6.0, 6.0, 6.0, 5.0, 7.0, 7.0]
        b = [5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 6.0, 2.0, 3.0, 6.0, 2.0, 5.0, 5.0, 6.0, 4.0, 6.0, 4.0, 5.0, 5.0, 3.0, 7.0, 5.0, 6.0, 6.0, 4.0, 3.0, 4.0, 3.0, 2.0, 4.0, 5.0, 4.0, 4.0, 6.0, 2.0, 6.0, 7.0, 4.0, 4.0, 5.0, 5.0, 5.0, 5.0, 7.0, 4.0, 5.0, 3.0, 2.0, 6.0, 7.0]

        r = rtests.r_wilcoxsign_test(a, b, print_result=True)

        """Test2 Result:
            Exact Wilcoxon-Pratt Signed-Rank Test
        data:  y by x (pos, neg) 
             stratified by block
        Z = 4.5276, p-value = 1.474e-06"""

        assert r["p_value"] == 1.474e-06