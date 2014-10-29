import unittest


from expressions.functions import _argument_sender, _MakeCallable


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

    def test__MakeCallable(self):
        double = _MakeCallable(2*x for x in _MakeCallable)
        self.assertEqual(8, double(4))

if __name__ == '__main__':
    unittest.main()