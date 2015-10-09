#!/usr/bin/env python

import sys
from fractions import gcd
from munkres import Munkres, make_cost_matrix

def is_vowel(char):
    return char.lower() in ['a', 'e', 'i', 'o', 'u']

def vowel_count(str):
    return len(filter(is_vowel, str))
    
def is_consonant(char):
    return char.lower() in ['b', 'c', 'd', 'f', 'g', 'h', 'j',
                            'k', 'l', 'm', 'n', 'p', 'q', 'r',
                            's', 't', 'v', 'w', 'x', 'y', 'z']

def consonant_count(str):
    return len(filter(is_consonant, str))

def funky_ctr(advertiser, person):
    if len(advertiser) % 2 == 0:
        base_ctr = 1.5 * vowel_count(person)
    else:
        base_ctr = consonant_count(person)

    if gcd(len(advertiser), len(person)) > 1:
        return 1.5 * base_ctr
    else:
        return base_ctr

def make_ctr_matrix(advertisers, persons, ctrfunc):
    # this is a list of lists

    # helper function for the map call below
    def make_row(advertiser):
        return map(lambda person: ctrfunc(advertiser, person), persons)

    return map(make_row, advertisers)

def make_match(advertisers, persons, ctrfunc = funky_ctr):
    # make the ctr matrix
    ctr_matrix = make_ctr_matrix(advertisers, persons, ctrfunc)

    # convert it to a cost matrix by subtracting all values from a larger value
    cost_matrix = make_cost_matrix(ctr_matrix, lambda ctr: sys.maxsize - ctr)

    # compute the match
    match = Munkres().compute(cost_matrix)

    # elements in match are two-element lists, where the first is the
    # index into advertisers and second is index into persons

    # compute the total ctr by looking up the match elements in the ctr
    # matrix
    total_ctr = sum(map(lambda pair: ctr_matrix[pair[0]][pair[1]], match))

    return match, total_ctr

def read_strings_from_file(filename):
    with open(filename) as f:
        return [x.strip('\n') for x in f.readlines()]

if __name__ == '__main__':
    # validate command line args
    if len(sys.argv) != 3:
        print "usage: %s <advertisers-file> <persons-file>" % sys.argv[0]
        sys.exit(0)

    advertisers = read_strings_from_file(sys.argv[1])
    persons     = read_strings_from_file(sys.argv[2])

    match, total_ctr = make_match(advertisers, persons)
    
    for a_index, p_index in match:
        print "%-46s %s" % (advertisers[a_index], persons[p_index])

    print "total_ctr is %d" % total_ctr
