# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.


import unittest

import extypes

class ConstrainedSetTests(unittest.TestCase):
    def test_instantiate(self):
        noname = extypes.ConstrainedSet(['a', 'b', 'c'])
        self.assertEqual('ConstrainedSet', noname.name)
        self.assertEqual(['a', 'b', 'c'], noname.choices)

        pretty = extypes.ConstrainedSet(['a', 'b', 'c'], name='Shiny')
        self.assertEqual('Shiny', pretty.name)
        self.assertEqual('Shiny', pretty.__name__)

    def test_set_operations(self):
        Foods = extypes.ConstrainedSet(['spam', 'eggs', 'bacon'], name='Foods')
        Cooking = extypes.ConstrainedSet(['cook', 'burn'], name='Cooking')
        fridge = Foods(['spam', 'bacon'])

        self.assertTrue('spam' in fridge)
        self.assertTrue('eggs' not in fridge)
        self.assertEqual(2, len(fridge))
        self.assertTrue(fridge)
        self.assertFalse(Foods())
        # ConstrainedSet retain the ordering of the constrainer
        self.assertEqual(['spam', 'bacon'], list(fridge))

        # Equality
        self.assertEqual(fridge, Foods(['spam', 'bacon']))
        # Equality doesn't care about ordering
        self.assertEqual(fridge, Foods(['spam', 'bacon']))
        self.assertNotEqual(fridge, Foods(['spam']))

        # Compare with other types
        self.assertFalse(Foods() == Cooking())
        self.assertTrue(Foods() != Cooking())

        # Set operations
        meat = Foods(['spam', 'bacon'])
        fresh = Foods(['eggs', 'bacon'])
        white = Foods(['eggs'])

        # Comparison
        self.assertTrue(meat.isdisjoint(white))
        self.assertTrue(white.isdisjoint(meat))

        self.assertTrue(white.issubset(fresh))
        self.assertTrue(white <= fresh)
        self.assertFalse(meat.issubset(fresh))
        self.assertFalse(meat <= fresh)
        self.assertTrue(white < fresh)
        self.assertFalse(white < white)

        self.assertTrue(fresh.issuperset(white))
        self.assertTrue(fresh >= white)
        self.assertFalse(fresh.issuperset(meat))
        self.assertFalse(fresh >= meat)
        self.assertTrue(fresh > white)
        self.assertFalse(white > white)

        # Combination
        self.assertEqual(Foods(['spam', 'bacon', 'eggs']), meat.union(fresh))
        self.assertEqual(Foods(['spam', 'bacon', 'eggs']), meat | fresh)
        self.assertEqual(fresh, fresh | white)

        self.assertEqual(Foods(['bacon']), meat.intersection(fresh))
        self.assertEqual(Foods(['bacon']), meat & fresh)
        self.assertEqual(white, fresh & white)

        self.assertEqual(Foods(['bacon']), fresh.difference(white))
        self.assertEqual(Foods(['bacon']), fresh - white)
        self.assertEqual(white, fresh - meat)

        self.assertEqual(Foods(['spam', 'eggs']), fresh.symmetric_difference(meat))
        self.assertEqual(Foods(['spam', 'eggs']), fresh ^ meat)
        self.assertEqual(Foods(['bacon']), white ^ fresh)

        # Copy
        meat2 = meat.copy()
        self.assertEqual(meat, meat2)
        meat2.add('eggs')
        self.assertNotEqual(meat, meat2)

        # Edition: add/remove/pop/clear
        meat2 = meat.copy()
        meat2.add('eggs')
        self.assertEqual(Foods(['eggs', 'spam', 'bacon']), meat2)

        # Involutive add
        meat2 = meat.copy()
        meat2.add('spam')
        self.assertEqual(meat, meat2)

        meat2 = meat.copy()
        meat2.remove('spam')
        self.assertEqual(Foods(['bacon']), meat2)

        meat2 = meat.copy()
        with self.assertRaises(KeyError):
            meat2.remove('eggs')
        self.assertIsNone(meat2.discard('eggs'))

        meat2 = meat.copy()
        meat2.discard('bacon')
        self.assertEqual(Foods(['spam']), meat2)

        meat2 = meat.copy()
        elem1 = meat2.pop()
        self.assertEqual(1, len(meat2))
        elem2 = meat2.pop()
        self.assertEqual(Foods(), meat2)
        self.assertEqual(set(['spam', 'bacon']), set([elem1, elem2]))

        meat2 = meat.copy()
        meat2.clear()
        self.assertEqual(Foods(), meat2)

        # Edition: update
        meat2 = meat.copy()
        meat2.update(white)
        self.assertEqual(Foods(['spam', 'eggs', 'bacon']), meat2)

        meat2 = meat.copy()
        meat2 |= fresh
        self.assertEqual(Foods(['spam', 'eggs', 'bacon']), meat2)

        # Edition: intersection update
        meat2 = meat.copy()
        meat2.intersection_update(fresh)
        self.assertEqual(Foods(['bacon']), meat2)

        fresh2 = fresh.copy()
        fresh2 &= white
        self.assertEqual(white, fresh2)

        # Edition: symmetric difference update
        meat2 = meat.copy()
        meat2.symmetric_difference_update(fresh)
        self.assertEqual(Foods(['eggs', 'spam']), meat2)

        fresh2 = fresh.copy()
        fresh2 ^= white
        self.assertEqual(Foods(['bacon']), fresh2)




if __name__ == '__main__':
    unittest.main()
