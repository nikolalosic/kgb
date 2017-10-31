from __future__ import unicode_literals

import unittest

from kgb.agency import SpyAgency
from kgb.spies import FunctionSpy
from kgb.tests.base import MathClass, TestCase


class SpyAgencyTests(TestCase):
    """Unit tests for kgb.agency.SpyAgency."""

    def test_spy_on(self):
        """Testing SpyAgency.spy_on"""
        obj = MathClass()

        spy = self.agency.spy_on(obj.do_math)
        self.assertEqual(self.agency.spies, [spy])

    def test_unspy(self):
        """Testing SpyAgency.unspy"""
        obj = MathClass()
        orig_do_math = obj.do_math

        spy = self.agency.spy_on(obj.do_math)
        self.assertEqual(self.agency.spies, [spy])

        self.agency.unspy(obj.do_math)
        self.assertEqual(self.agency.spies, [])

        self.assertEqual(obj.do_math, orig_do_math)

    def test_unspy_all(self):
        """Testing SpyAgency.unspy_all"""
        obj = MathClass()
        orig_do_math = obj.do_math

        spy1 = self.agency.spy_on(obj.do_math)
        spy2 = self.agency.spy_on(MathClass.class_do_math)

        self.assertEqual(self.agency.spies, [spy1, spy2])

        self.agency.unspy_all()
        self.assertEqual(self.agency.spies, [])

        self.assertEqual(obj.do_math, orig_do_math)
        self.assertEqual(MathClass.class_do_math, self.orig_class_do_math)


class MixinTests(SpyAgency, unittest.TestCase):
    def test_spy_on(self):
        """Testing SpyAgency mixed in with spy_on"""
        obj = MathClass()

        self.spy_on(obj.do_math)
        self.assertTrue(isinstance(obj.do_math, FunctionSpy))

        result = obj.do_math()
        self.assertEqual(result, 3)

    def test_tear_down(self):
        """Testing SpyAgency mixed in with tearDown"""
        obj = MathClass()
        orig_do_math = obj.do_math

        self.spy_on(obj.do_math)
        self.assertTrue(isinstance(obj.do_math, FunctionSpy))

        self.tearDown()

        self.assertEqual(obj.do_math, orig_do_math)
