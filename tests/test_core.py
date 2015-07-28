import unittest
from symbolic.core import (MatrixType, argument_sender, CallableObject,
                           Expression, Eq, Ne, Lt, Le, Gt, Ge)


class MatrixTypeSuite(unittest.TestCase):
    def test_MatrixType_vector(self):
        v = MatrixType([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test_MatrixType_vector_interface(self):
        """Should define a 3-vector of numbers"""
        u = MatrixType**3;
        self.assertEqual(u._array, MatrixType([0, 0, 0])._array)

    def test_MatrixType_matrix(self):
        A = MatrixType([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_MatrixType_matrix_interface(self):
        A = MatrixType**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_MatrixType_matrix_getitem(self):
        A = MatrixType([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions_MatrixType_matrix_interface(self):
        A = MatrixType**3*3*2
        array = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                 [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.assertEqual(A._array, array)


class FunctionSuite(unittest.TestCase):
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
        double = CallableObject(x*2 for x in MatrixType)
        self.assertEqual(8, next(double(4)))

    def test_many_variables(self):
        add = MatrixType(x + y for x, y in MatrixType)
        added = add(3, 4)
        self.assertEqual(7, next(added))

    def test_CallableObject_string(self):
        """Should make a correct code if use some CallableObject object."""
        double = MatrixType(x*2 for x in MatrixType)
        expr = MatrixType(double(y) for y in MatrixType)
        self.assertEqual(expr.__expr__, 'double(y)')

    def test_CallableObject_string_with_many_variables(self):
        """Should make a correct code if use some CallableObject object."""
        add = MatrixType(x + y for (x, y) in MatrixType)
        expr = MatrixType(add(x, y) + add(1, 2) for (x, y) in MatrixType)
        self.assertEqual(expr.__expr__, 'add(x, y)+(add(1, 2))')

    def test_eval_method(self):
        cube = MatrixType(x**3 for x in MatrixType)
        self.assertEqual(27, cube.eval(3))

    def test_eval_method_with_many_variables(self):
        pow = MatrixType(x**y for (x, y) in MatrixType)
        self.assertEqual(27, pow.eval(3, 3))


class ExpressionSuite(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.var = Expression('var')

    # Left operators

    def test_left_add_operator(self):
        self.assertEqual((self.var + 2).__expr__, 'var+(2)')

    def test_left_and_operator(self):
        self.assertEqual((self.var & 2).__expr__, 'var&(2)')

    def test_left_div_operator(self):
        self.assertEqual((self.var / 2).__expr__, 'var/(2)')

    def test_left_eq_operator(self):
        self.assertEqual((self.var == 2).__expr__, 'var==(2)')

    def test_left_floordiv_operator(self):
        self.assertEqual((self.var // 2).__expr__, 'var//(2)')

    def test_left_ge_operator(self):
        self.assertEqual((self.var >= 2).__expr__, 'var>=(2)')

    def test_left_gt_operator(self):
        self.assertEqual((self.var > 2).__expr__, 'var>(2)')

    def test_left_le_operator(self):
        self.assertEqual((self.var <= 2).__expr__, 'var<=(2)')

    def test_left_lshift_operator(self):
        self.assertEqual((self.var << 2).__expr__, 'var<<(2)')

    def test_left_lt_operator(self):
        self.assertEqual((self.var < 2).__expr__, 'var<(2)')

    def test_left_matmul_operator(self):
        self.assertEqual((self.var @ 2).__expr__, 'var@(2)')

    def test_left_mod_operator(self):
        self.assertEqual((self.var % 2).__expr__, 'var%(2)')

    def test_left_mul_operator(self):
        self.assertEqual((self.var * 2).__expr__, 'var*(2)')

    def test_left_ne_operator(self):
        self.assertEqual((self.var != 2).__expr__, 'var!=(2)')

    def test_left_or_operator(self):
        self.assertEqual((self.var | 2).__expr__, 'var|(2)')

    def test_left_pow_operator(self):
        self.assertEqual((self.var ** 2).__expr__, 'var**(2)')

    def test_left_rshift_operator(self):
        self.assertEqual((self.var >> 2).__expr__, 'var>>(2)')

    def test_left_sub_operator(self):
        self.assertEqual((self.var - 2).__expr__, 'var-(2)')

    def test_left_truediv_operator(self):
        self.assertEqual((self.var / 2).__expr__, 'var/(2)')

    def test_left_xor_operator(self):
        self.assertEqual((self.var ^ 2).__expr__, 'var^(2)')

    # Right operators

    def test_right_radd_operator(self):
        self.assertEqual((2 + self.var).__expr__, '(2)+var')

    def test_right_rand_operator(self):
        self.assertEqual((2 & self.var).__expr__, '(2)&var')

    def test_right_rdiv_operator(self):
        self.assertEqual((2 / self.var).__expr__, '(2)/var')

    def test_rflooright_rfloordiv_operator(self):
        self.assertEqual((2 // self.var).__expr__, '(2)//var')

    def test_rlsright_rlshift_operator(self):
        self.assertEqual((2 << self.var).__expr__, '(2)<<var')

    def test_rmaright_rmatmul_operator(self):
        self.assertEqual((2 @ self.var).__expr__, '(2)@var')

    def test_right_rmod_operator(self):
        self.assertEqual((2 % self.var).__expr__, '(2)%var')

    def test_right_rmul_operator(self):
        self.assertEqual((2 * self.var).__expr__, '(2)*var')

    def test_right_ror_operator(self):
        self.assertEqual((2 | self.var).__expr__, '(2)|var')

    def test_right_rpow_operator(self):
        self.assertEqual((2 ** self.var).__expr__, '(2)**var')

    def test_right_rrshift_operator(self):
        self.assertEqual((2 >> self.var).__expr__, '(2)>>var')

    def test_right_rsub_operator(self):
        self.assertEqual((2 - self.var).__expr__, '(2)-var')

    def test_right_rtruediv_operator(self):
        self.assertEqual((2 / self.var).__expr__, '(2)/var')

    def test_right_rxor_operator(self):
        self.assertEqual((2 ^ self.var).__expr__, '(2)^var')

    # Unary operators

    def test_invert_unary_operator(self):
        self.assertEqual((~self.var).__expr__, '~(var)')

    def test_neg_unary_operator(self):
        self.assertEqual((-self.var).__expr__, '-(var)')

    def test_pos_unary_operator(self):
        self.assertEqual((+self.var).__expr__, '+(var)')

    # Built in functions

    def test_abs_built_in_function(self):
        self.assertEqual((abs(self.var)).__expr__, 'abs(var)')

    def test_round_built_in_function(self):
        self.assertEqual((round(self.var, 2)).__expr__, 'round(var, 2)')

    def test_reversed_built_in_function(self):
        self.assertEqual(reversed(self.var).__expr__, 'reversed(var)')

    # Attribute and item access

    def test__getitem__method(self):
        self.assertEqual(self.var[1].__expr__, "(var)[1]")
        self.assertEqual(self.var[1, 2].__expr__, "(var)[(1, 2)]")
        self.assertEqual(self.var['key'].__expr__, "(var)['key']")

    def test__repr__method(self):
        self.assertEqual(repr(self.var), "var")

    def test__call__method(self):
        x = Expression('x')
        y = Expression('y')
        z = Expression('z')
        self.assertEqual(self.var(x, y, z), "var(x, y, z)")
        self.assertEqual(self.var(0, 0, 0), "var(0, 0, 0)")


# This class is not runned if not inherit from unittest.TestCase
# class FailedExpressionBehaviours(unittest.TestCase):
class FailedExpressionSuite:
    @classmethod
    def setUpClass(self):
        var = Expression('var')

    @unittest.expectedFailure
    def test_len_built_in_function(self):
        "TypeError: 'Expression' object cannot let interpreted as an integer"
        self.assertEqual(len(var).__expr__, 'len(var)')

    @unittest.expectedFailure
    def test_iter_built_in_function(self):
        """TypeError: iter() returned non-iterator of type 'Expression'"""
        self.assertEqual(iter(var).__expr__, 'iter(var)')

    @unittest.expectedFailure
    def test_contains_built_in_function(self):
        "TypeError: 'Expression' object cannot let interpreted as an integer"
        self.assertEqual(('item' in var).__expr__,
                         "('item' in var)")

    @unittest.expectedFailure
    def test_isinstance_built_in_function(self):
        """AttributeError: 'bool' object has no attribute '__expr__'"""
        self.assertEqual(isinstance(var, type).__expr__,
                         'isinstance(var, type)')

    @unittest.expectedFailure
    def test_issubclass_built_in_function(self):
        """TypeError: issubclass() arg 1 must let a class"""
        self.assertEqual(issubclass(var, type).__expr__,
                         'issubclass(var, type)')


class EqClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Eq), "==")

    def test_operations(self):
        self.assertEqual(Eq, +Eq)
        self.assertEqual(Eq, -Eq)
        self.assertEqual(Eq, Eq + 1)
        self.assertEqual(Eq, 2 + Eq)
        self.assertEqual(Eq, Eq - 3)
        self.assertEqual(Eq, Eq/5)
        self.assertEqual(Eq, 6/Eq)
        self.assertEqual(Eq, Eq*7)
        self.assertEqual(Eq, 8*Eq)
        self.assertEqual(Eq, 4 - Eq)
        self.assertEqual(Eq, Eq/(-9))
        self.assertEqual(Eq, (-10)/Eq)
        self.assertEqual(Eq, Eq*(-11))
        self.assertEqual(Eq, (-12)*Eq)


class EqInstanceSuite(unittest.TestCase):
    def test_order(self):
        eq1 = Eq('x', 1)
        self.assertEqual(eq1.left, 'x')
        self.assertEqual(eq1.right, 1)
        eq2 = Eq(2, 'x')
        self.assertEqual(eq2.left, 'x')
        self.assertEqual(eq2.right, 2)

    def test_repr(self):
        self.assertEqual(repr(Eq('x', 5)), "x == 5")
        self.assertEqual(repr(Eq('x', 5.0)), "x == 5.0")
        self.assertEqual(repr(Eq('x', 5.0 + 3.5j)), "x == (5+3.5j)")

    def test_operations(self):
        eq = Eq('y', 10)
        self.assertEqual(eq, +eq)
        self.assertEqual(eq, -eq)
        self.assertEqual(eq, eq + 1)
        self.assertEqual(eq, 2 + eq)
        self.assertEqual(eq, eq - 3)
        self.assertEqual(eq, eq/5)
        self.assertEqual(eq, 6/eq)
        self.assertEqual(eq, eq*7)
        self.assertEqual(eq, 8*eq)
        self.assertEqual(eq, 4 - eq)
        self.assertEqual(eq, eq/(-9))
        self.assertEqual(eq, (-10)/eq)
        self.assertEqual(eq, eq*(-11))
        self.assertEqual(eq, (-12)*eq)


class NeClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Ne), "!=")

    def test_operations(self):
        self.assertEqual(Ne, +Ne)
        self.assertEqual(Ne, -Ne)
        self.assertEqual(Ne, Ne + 1)
        self.assertEqual(Ne, 2 + Ne)
        self.assertEqual(Ne, Ne - 3)
        self.assertEqual(Ne, 4 - Ne)
        self.assertEqual(Ne, Ne/5)
        self.assertEqual(Ne, 6/Ne)
        self.assertEqual(Ne, Ne*7)
        self.assertEqual(Ne, 8*Ne)
        self.assertEqual(Ne, Ne/(-9))
        self.assertEqual(Ne, (-10)/Ne)
        self.assertEqual(Ne, Ne*(-11))
        self.assertEqual(Ne, (-12)*Ne)


class NeInstanceSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Ne('x', 5)), "x != 5")
        self.assertEqual(repr(Ne('x', 5.0)), "x != 5.0")
        self.assertEqual(repr(Ne('x', 5.0 + 3.5j)), "x != (5+3.5j)")

    def test_operations(self):
        ne = Ne('y', 10)
        self.assertEqual(ne, +ne)
        self.assertEqual(ne, -ne)
        self.assertEqual(ne, ne + 1)
        self.assertEqual(ne, 2 + ne)
        self.assertEqual(ne, ne - 3)
        self.assertEqual(ne, 4 - ne)
        self.assertEqual(ne, ne/5)
        self.assertEqual(ne, 6/ne)
        self.assertEqual(ne, ne*7)
        self.assertEqual(ne, 8*ne)
        self.assertEqual(ne, ne/(-9))
        self.assertEqual(ne, (-10)/ne)
        self.assertEqual(ne, ne*(-11))
        self.assertEqual(ne, (-12)*ne)


class LtClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Lt), "<")

    def test_operations(self):
        self.assertEqual(Lt, -Gt)
        self.assertEqual(Lt, 1 - Gt)
        self.assertEqual(Lt, Gt/(-2))
        self.assertEqual(Lt, (-3)/Gt)
        self.assertEqual(Lt, Gt*(-4))
        self.assertEqual(Lt, (-5)*Gt)


class LtInstanceSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Lt('x', 5)), "x < 5")
        self.assertEqual(repr(Lt('x', 5.0)), "x < 5.0")
        self.assertEqual(repr(Lt('x', 5.0 + 3.5j)), "x < (5+3.5j)")

    def test_operations(self):
        lt = Lt('y', 10)
        gt = Gt('y', 10)
        self.assertEqual(lt, -gt)
        self.assertEqual(lt, 1 - gt)
        self.assertEqual(lt, gt/(-2))
        self.assertEqual(lt, (-3)/gt)
        self.assertEqual(lt, gt*(-4))
        self.assertEqual(lt, (-5)*gt)


class GtClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Gt), ">")

    def test_operations(self):
        self.assertEqual(Gt, -Lt)
        self.assertEqual(Gt, 1 - Lt)
        self.assertEqual(Gt, Lt/(-2))
        self.assertEqual(Gt, (-3)/Lt)
        self.assertEqual(Gt, Lt*(-4))
        self.assertEqual(Gt, (-5)*Lt)


class GtInstanceSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Gt('x', 5)), "x > 5")
        self.assertEqual(repr(Gt('x', 5.0)), "x > 5.0")
        self.assertEqual(repr(Gt('x', 5.0 + 3.5j)), "x > (5+3.5j)")

    def test_operations(self):
        lt = Lt('y', 10)
        gt = Gt('y', 10)
        self.assertEqual(gt, -lt)
        self.assertEqual(gt, 1 - lt)
        self.assertEqual(gt, lt/(-2))
        self.assertEqual(gt, (-3)/lt)
        self.assertEqual(gt, lt*(-4))
        self.assertEqual(gt, (-5)*lt)


class LeClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Le), "<=")

    def test_operations(self):
        self.assertEqual(Le, -Ge)
        self.assertEqual(Le, 1 - Ge)
        self.assertEqual(Le, Ge/(-2))
        self.assertEqual(Le, (-3)/Ge)
        self.assertEqual(Le, Ge*(-4))
        self.assertEqual(Le, (-5)*Ge)

class LeInstanceSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Le('x', 5)), "x <= 5")
        self.assertEqual(repr(Le('x', 5.0)), "x <= 5.0")
        self.assertEqual(repr(Le('x', 5.0 + 3.5j)), "x <= (5+3.5j)")

    def test_operations(self):
        le = Le('y', 10)
        ge = Ge('y', 10)
        self.assertEqual(le, -ge)
        self.assertEqual(le, 1 - ge)
        self.assertEqual(le, ge/(-2))
        self.assertEqual(le, (-3)/ge)
        self.assertEqual(le, ge*(-4))
        self.assertEqual(le, (-5)*ge)


class GeClassSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Ge), ">=")

    def test_operations(self):
        self.assertEqual(Ge, -Le)
        self.assertEqual(Ge, 1 - Le)
        self.assertEqual(Ge, Le/(-2))
        self.assertEqual(Ge, (-3)/Le)
        self.assertEqual(Ge, Le*(-4))
        self.assertEqual(Ge, (-5)*Le)


class GeInstanceSuite(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Ge('x', 5)), "x >= 5")
        self.assertEqual(repr(Ge('x', 5.0)), "x >= 5.0")
        self.assertEqual(repr(Ge('x', 5.0 + 3.5j)), "x >= (5+3.5j)")

    def test_operations(self):
        ge = Ge('y', 10)
        le = Le('y', 10)
        self.assertEqual(ge, -le)
        self.assertEqual(ge, 1 - le)
        self.assertEqual(ge, le/(-2))
        self.assertEqual(ge, (-3)/le)
        self.assertEqual(ge, le*(-4))
        self.assertEqual(ge, (-5)*le)
