import unittest
from symbolicmath.core import (BaseType, argument_sender, CallableObject,
    ExpressionString)


class TestBaseTypeType(unittest.TestCase):
    def test_BaseType_vector(self):
        v = BaseType([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test_BaseType_vector_interface(self):
        """Should define a 3-vector of numbers"""
        u = BaseType**3;
        self.assertEqual(u._array, BaseType([0, 0, 0])._array)

    def test_BaseType_matrix(self):
        A = BaseType([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_BaseType_matrix_interface(self):
        A = BaseType**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_BaseType_matrix_getitem(self):
        A = BaseType([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions_BaseType_matrix_interface(self):
        A = BaseType**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)


class FunctionTest(unittest.TestCase):
    def test_argument_sender(self):
        """The coroutine object created with argument_sender should
        yield the value sended and return the value again in the next
        iteration."""
        sender = argument_sender()
        next(sender)
        a = sender.send(2)
        b = next(sender)
        self.assertEqual(a, 2)
        self.assertEqual(b, 2)

    def test_CallableObject(self):
        double = CallableObject(x*2 for x in BaseType)
        self.assertEqual(8, next(double(4)))

    def test_many_variables(self):
        add = BaseType(x + y for x, y in BaseType)
        added = add(3, 4)
        self.assertEqual(7, next(added))


class ExpressionTest(unittest.TestCase):
    def test_bynary_left_operators(self):
        add = BaseType(x+2 for x in BaseType)
        and_ = BaseType(x&2 for x in BaseType)
        div = BaseType(x/2 for x in BaseType)
        eq = BaseType(x==2 for x in BaseType)
        floordiv = BaseType(x//2 for x in BaseType)
        ge = BaseType(x>=2 for x in BaseType)
        gt = BaseType(x>2 for x in BaseType)
        le = BaseType(x<=2 for x in BaseType)
        lshift = BaseType(x<<2 for x in BaseType)
        lt = BaseType(x<2 for x in BaseType)
        # matmul = BaseType(x@2 for x in BaseType)
        mod = BaseType(x%2 for x in BaseType)
        mul = BaseType(x*2 for x in BaseType)
        ne = BaseType(x!=2 for x in BaseType)
        # or_ = BaseType(x|2 for x in BaseType)
        pow = BaseType(x**2 for x in BaseType)
        rshift = BaseType(x>>2 for x in BaseType)
        sub = BaseType(x-2 for x in BaseType)
        truediv = BaseType(x/2 for x in BaseType)
        xor = BaseType(x^2 for x in BaseType)

        self.assertEqual(add._expression, 'x+(2)')
        self.assertEqual(and_._expression, 'x&(2)')
        self.assertEqual(div._expression, 'x/(2)')
        self.assertEqual(eq._expression, 'x==(2)')
        self.assertEqual(floordiv._expression, 'x//(2)')
        self.assertEqual(ge._expression, 'x>=(2)')
        self.assertEqual(gt._expression, 'x>(2)')
        self.assertEqual(le._expression, 'x<=(2)')
        self.assertEqual(lshift._expression, 'x<<(2)')
        self.assertEqual(lt._expression, 'x<(2)')
        # self.assertEqual(matmul._expression, 'x@(2)')
        self.assertEqual(mod._expression, 'x%(2)')
        self.assertEqual(mul._expression, 'x*(2)')
        self.assertEqual(ne._expression, 'x!=(2)')
        # self.assertEqual(or_._expression, 'x|(2)')
        self.assertEqual(pow._expression, 'x**(2)')
        self.assertEqual(rshift._expression, 'x>>(2)')
        self.assertEqual(sub._expression, 'x-(2)')
        self.assertEqual(truediv._expression, 'x/(2)')
        self.assertEqual(xor._expression, 'x^(2)')

    def test_bynary_right_operators(self):
        radd = BaseType(2+x for x in BaseType)
        rand = BaseType(2&x for x in BaseType)
        rdiv = BaseType(2/x for x in BaseType)
        rfloordiv = BaseType(2//x for x in BaseType)
        rlshift = BaseType(2<<x for x in BaseType)
        # rmatmul = BaseType(2@x for x in BaseType)
        rmod = BaseType(2%x for x in BaseType)
        rmul = BaseType(2*x for x in BaseType)
        # ror_ = BaseType(2|x for x in BaseType)
        rpow = BaseType(2**x for x in BaseType)
        rrshift = BaseType(2>>x for x in BaseType)
        rsub = BaseType(2-x for x in BaseType)
        rtruediv = BaseType(2/x for x in BaseType)
        rxor = BaseType(2^x for x in BaseType)

        self.assertEqual(radd._expression, '(2)+x')
        self.assertEqual(rand._expression, '(2)&x')
        self.assertEqual(rdiv._expression, '(2)/x')
        self.assertEqual(rfloordiv._expression, '(2)//x')
        self.assertEqual(rlshift._expression, '(2)<<x')
        # self.assertEqual(rmatmul._expression, '(2)@x')
        self.assertEqual(rmod._expression, '(2)%x')
        self.assertEqual(rmul._expression, '(2)*x')
        # self.assertEqual(ror_._expression, '(2)|x')
        self.assertEqual(rpow._expression, '(2)**x')
        self.assertEqual(rrshift._expression, '(2)>>x')
        self.assertEqual(rsub._expression, '(2)-x')
        self.assertEqual(rtruediv._expression, '(2)/x')
        self.assertEqual(rxor._expression, '(2)^x')

    def test_unary_operators(self):
        invert = BaseType(~x for x in BaseType)
        neg = BaseType(-x for x in BaseType)
        pos = BaseType(+x for x in BaseType)

        self.assertEqual(invert._expression, '~(x)')
        self.assertEqual(neg._expression, '-(x)')
        self.assertEqual(pos._expression, '+(x)')

    def test___name__property(self):
        """The BaseType() instance shoud have the __name__ property."""
        named_lambda = BaseType(+x for x in BaseType)
        self.assertEqual(named_lambda.__name__, 'named_lambda')

    def testCallableObject_string(self):
        """Should make a correct code if use some CallableObject object."""
        double = BaseType(x*2 for x in BaseType)
        expr = BaseType(double(y) for y in BaseType)
        self.assertEqual(expr._expression, 'double(y)')


if __name__ == '__main__':
    unittest.main()