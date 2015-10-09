import unittest
from ad_matcher import funky_ctr, make_match

class AdMatcherTest(unittest.TestCase):
    # test our funky ctr function under all configurations of:
    #   parity of advertiser length
    #   whether advertiser length and person length have a common factor 
    def test_even_no_factor(self):
        self.assertEqual(1.5 * 3, funky_ctr('12', 'uUu'))

    def test_even_factor(self):
        self.assertEqual(1.5 * 1.5 * 2, funky_ctr('12', 'uU'))

    def test_odd_no_factor(self):
        self.assertEqual(2, funky_ctr('123', 'zZ'))

    def test_odd_factor(self):
        self.assertEqual(1.5 * 6, funky_ctr('123', 'zZzZzZ'))

    # test the matching functionality using a simpler ctr function:
    # product of the lengths of the advertiser and the person. we know
    # the sum of squares is maximal.
    def test_matching(self):
        advertisers = ['1', '22', '333', '4444', '55555']
        persons     = ['ccc', 'eeeee', 'a', 'dddd', 'bb']

        def alternative_ctr(advertiser, person):
            return len(advertiser) * len(person)
        
        match, total_ctr = make_match(advertisers, persons, alternative_ctr)
        self.assertEqual(1 * 1 + 2 * 2 + 3 * 3 + 4 * 4 + 5 * 5, total_ctr)
        for a_index, p_index in match:
            self.assertEqual(len(advertisers[a_index]), len(persons[p_index]))
        
if __name__ == '__main__':
    unittest.main()
