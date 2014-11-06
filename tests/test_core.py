import unittest
from expressions.core import (_TypeMaker, _argument_sender, _CallableMaker,
    _MakeExpressionString)


class Test_TypeMakerType(unittest.TestCase):
    def test__TypeMaker_vector(self):
        v = _TypeMaker([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test__TypeMaker_vector_interface(self):
        """Should define a 3-vector of numbers"""
        u = _TypeMaker**3;
        self.assertEqual(u._array, _TypeMaker([0, 0, 0])._array)

    def test__TypeMaker_matrix(self):
        A = _TypeMaker([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test__TypeMaker_matrix_interface(self):
        A = _TypeMaker**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test__TypeMaker_matrix_getitem(self):
        A = _TypeMaker([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions__TypeMaker_matrix_interface(self):
        A = _TypeMaker**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)


class FunctionTest(unittest.TestCase):
    def test__argument_sender(self):
        """The coroutine object created with _argument_sender should
        yield the value sended and return the value again in the next
        iteration."""
        sender = _argument_sender()
        next(sender)
        a = sender.send(2)
        b = next(sender)
        self.assertEqual(a, 2)
        self.assertEqual(b, 2)

    def test__CallableMaker(self):
        double = _CallableMaker(x*2 for x in _TypeMaker)
        self.assertEqual(8, next(double(4)))


class ExpressionTest(unittest.TestCase):
    def test_bynary_left_operators(self):
        add = _TypeMaker(x+2 for x in _TypeMaker)
        and_ = _TypeMaker(x&2 for x in _TypeMaker)
        div = _TypeMaker(x/2 for x in _TypeMaker)
        eq = _TypeMaker(x==2 for x in _TypeMaker)
        floordiv = _TypeMaker(x//2 for x in _TypeMaker)
        ge = _TypeMaker(x>=2 for x in _TypeMaker)
        gt = _TypeMaker(x>2 for x in _TypeMaker)
        le = _TypeMaker(x<=2 for x in _TypeMaker)
        lshift = _TypeMaker(x<<2 for x in _TypeMaker)
        lt = _TypeMaker(x<2 for x in _TypeMaker)
        # matmul = _TypeMaker(x@2 for x in _TypeMaker)
        mod = _TypeMaker(x%2 for x in _TypeMaker)
        mul = _TypeMaker(x*2 for x in _TypeMaker)
        ne = _TypeMaker(x!=2 for x in _TypeMaker)
        # or_ = _TypeMaker(x|2 for x in _TypeMaker)
        pow = _TypeMaker(x**2 for x in _TypeMaker)
        rshift = _TypeMaker(x>>2 for x in _TypeMaker)
        sub = _TypeMaker(x-2 for x in _TypeMaker)
        truediv = _TypeMaker(x/2 for x in _TypeMaker)
        xor = _TypeMaker(x^2 for x in _TypeMaker)

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
        radd = _TypeMaker(2+x for x in _TypeMaker)
        rand = _TypeMaker(2&x for x in _TypeMaker)
        rdiv = _TypeMaker(2/x for x in _TypeMaker)
        rfloordiv = _TypeMaker(2//x for x in _TypeMaker)
        rlshift = _TypeMaker(2<<x for x in _TypeMaker)
        # rmatmul = _TypeMaker(2@x for x in _TypeMaker)
        rmod = _TypeMaker(2%x for x in _TypeMaker)
        rmul = _TypeMaker(2*x for x in _TypeMaker)
        # ror_ = _TypeMaker(2|x for x in _TypeMaker)
        rpow = _TypeMaker(2**x for x in _TypeMaker)
        rrshift = _TypeMaker(2>>x for x in _TypeMaker)
        rsub = _TypeMaker(2-x for x in _TypeMaker)
        rtruediv = _TypeMaker(2/x for x in _TypeMaker)
        rxor = _TypeMaker(2^x for x in _TypeMaker)

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
        invert = _TypeMaker(~x for x in _TypeMaker)
        neg = _TypeMaker(-x for x in _TypeMaker)
        pos = _TypeMaker(+x for x in _TypeMaker)

        self.assertEqual(invert._expression, '~(x)')
        self.assertEqual(neg._expression, '-(x)')
        self.assertEqual(pos._expression, '+(x)')

    def test___name__property(self):
        """The _TypeMaker() instance shoud have the __name__ property."""
        named_lambda = _TypeMaker(+x for x in _TypeMaker)
        self.assertEqual(named_lambda.__name__, 'named_lambda')


if __name__ == '__main__':
    unittest.main()