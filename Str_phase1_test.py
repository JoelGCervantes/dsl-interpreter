# test_str_concat_replace.py

import unittest
from interp import Str, Concat, Replace, Lit, evalInEnv, emptyEnv, EvalError

class TestStrOperations(unittest.TestCase):

    # ---------- Str Tests ----------
    def test_str_repr(self):
        self.assertEqual(str(Str("hello")), "hello")
        self.assertEqual(str(Str("")), "")
        self.assertEqual(str(Str("123")), "123")

    def test_str_eq(self):
        self.assertTrue(Str("abc") == Str("abc"))
        self.assertFalse(Str("abc") == Str("def"))
        self.assertFalse(Str("abc") == "abc")  # different types

    # ---------- Concat Tests ----------
    def test_concat_basic(self):
        expr = Concat(Lit(Str("hello")), Lit(Str(" world")))
        result = evalInEnv(emptyEnv, expr)
        self.assertEqual(result, Str("hello world"))

    def test_concat_empty(self):
        expr = Concat(Lit(Str("")), Lit(Str("x")))
        result = evalInEnv(emptyEnv, expr)
        self.assertEqual(result, Str("x"))

    def test_concat_type_error(self):
        with self.assertRaises(EvalError):
            expr = Concat(Lit(Str("hello")), Lit(123))  # int is not Str
            evalInEnv(emptyEnv, expr)

    # ---------- Replace Tests ----------
    def test_replace_basic(self):
        expr = Replace(Lit(Str("hello")), Lit(Str("l")), Lit(Str("z")))
        result = evalInEnv(emptyEnv, expr)
        self.assertEqual(result, Str("hezlo"))  # only first 'l' replaced

    def test_replace_no_match(self):
        expr = Replace(Lit(Str("hello")), Lit(Str("x")), Lit(Str("z")))
        result = evalInEnv(emptyEnv, expr)
        self.assertEqual(result, Str("hello"))

    def test_replace_empty(self):
        expr = Replace(Lit(Str("")), Lit(Str("a")), Lit(Str("b")))
        result = evalInEnv(emptyEnv, expr)
        self.assertEqual(result, Str(""))

    def test_replace_type_error(self):
        with self.assertRaises(EvalError):
            expr = Replace(Lit(Str("abc")), Lit(1), Lit(Str("b")))  # old is not Str
            evalInEnv(emptyEnv, expr)

        with self.assertRaises(EvalError):
            expr = Replace(Lit(123), Lit(Str("1")), Lit(Str("2")))  # target is not Str
            evalInEnv(emptyEnv, expr)


if __name__ == "__main__":
    unittest.main()
