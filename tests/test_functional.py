import unittest

from symbolic.functional import Function, Parameters, inject_constants
from symbolic.core import where


_GLOBAL = 'GLOBAL'


class TestWhere(unittest.TestCase):
    def test_where_class_statement(self):
        obtained = (1, 2) &where(PI=3.14)
        expected = [{'PI': 3.14}, (1, 2)]
        self.assertEqual(obtained, expected)
        self.assertTrue(isinstance(obtained[0], where))

    def test_inject_constants_function(self):
        generator = ((x + a, y + b, z + c) for (x, y, z) in [[1, 2, 3]])
        expanded = inject_constants(generator, a=1, b=2, c=3)
        self.assertEqual((2, 4, 6), next(expanded))


class TestFunction(unittest.TestCase):
    def setUp(self):
        self.function = Function(x for x in Parameters)

    def test_instance(self):
        self.assertTrue(isinstance(self.function, Function))

    def test_basic_source_code(self):
        expected = "def function(x):\n"\
                   "    yield x"
        self.assertEqual(self.function.__source__, expected)

    def test_source_code_with_many_variables(self):
        function = Function((x, y, z) for (x, y, z) in Parameters)
        expected = "def function(x, y, z):\n"\
                   "    yield (x, y, z)"
        self.assertEqual(function.__source__, expected)

    def test_source_code_with_some_operations(self):
        function = Function(-x*y**z for (x, y, z) in Parameters)
        expected = "def function(x, y, z):\n"\
                   "    yield -(x)*(y**(z))"
        self.assertEqual(function.__source__, expected)

    def test_where_class(self):
        function = Function((PI*r**2) &where(PI=3.14) for r in Parameters)
        expected = "def function(r):\n"\
                   "    yield (3.14)*r**(2)"
        self.assertEqual(function.__source__, expected)

    def test_where_class_with_two_constants(self):
        function = Function(
            PI*r**two
        &where (
            PI = 3.14,
            two = 2
        ) for r in Parameters)
        expected = "def function(r):\n"\
                   "    yield (3.14)*r**(2)"
        self.assertEqual(function.__source__, expected)

    def test_where_class_with_global_var(self):
        function = Function(
            _GLOBAL
        &where(
            _GLOBAL='where_GLOBAL'
        ) for void in Parameters)

        expected = "def function(void):\n"\
                   "    yield 'where_GLOBAL'"
        self.assertEqual(function.__source__, expected)

    def test_where_class_with_local_var(self):
        a_local = 'a'
        b_local = 'b'

        function = Function(
            a_local+b_local
            &where (
                a_local = 'AA',
                b_local = 'BB',
            ) for _ in Parameters)

        expected = "def function(_):\n"\
                   "    yield 'AABB'"
        self.assertEqual(function.__source__, expected)

    def test_where_class_with_non_local_variables(self):
        non_local = '_nnnnnnn'

        function = Function(
            a_local+non_local
            &where (
                a_local = 'AA',
            ) for _ in Parameters)

        expected = "def function(_):\n"\
                   "    yield 'AA_nnnnnnn'"
        self.assertEqual(function.__source__, expected)

    @unittest.skip('unimplemented')
    def test_where_class_in_the_begining_of_the_expression(self):
        """Should raise an SintaxError if
        where is placed in the begining."""

    @unittest.skip('unimplemented')
    def test_where_class_in_the_middle_of_the_expression(self):
        """Should raise an SintaxError if
        where is placed in the middle."""

    @unittest.skip('unimplemented')
    def test_where_class_with_unary_operator(self):
        """Should raise an SintaxError if
        where have an unary operator."""

    @unittest.skip('unimplemented')
    def test_where_class_with_binary_left_operator(self):
        """Should raise an SintaxError if where is used
        with an binary operator placed in the left."""

    @unittest.skip('unimplemented')
    def test_where_class_with_binary_right_operator(self):
        """Should raise an SintaxError if where have
        an binary operator in the right side."""

    @unittest.skip('unimplemented')
    def test_CalledObject_instances_wrapped_with_next_method(self):
        """All `CalledObject` instances should be
        wrapped with the next() built-in method."""


if __name__ == '__main__':
    unittest.main()
