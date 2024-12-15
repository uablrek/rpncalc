import unittest
import rpn

# https://ongspxm.gitlab.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/

class Basic(unittest.TestCase):
    def test_stack(self):
        c = rpn.calc()
        with self.assertRaises(IndexError): c.pop()
        with self.assertRaises(IndexError): c.top()
        c.push(1)
        c.push(2)
        self.assertEqual(c.top(), 2)
        self.assertEqual(c.stack, [1, 2])
        self.assertEqual(c.pop(), 2)
        self.assertEqual(c.pop(), 1)
        with self.assertRaises(IndexError): c.pop()
        with self.assertRaises(IndexError): c.dup()
        c.push(1)
        c.dup()
        self.assertEqual(c.stack, [1, 1])
        c.clear()
        self.assertEqual(c.stack, [])
    def test_basic_arithmetic(self):
        c = rpn.calc()
        c.push(1)
        with self.assertRaises(IndexError): c.plus()
        c.push(1)
        c.push(2)
        self.assertEqual(c.stack, [1, 2])
        self.assertEqual(c.plus(), 3)
        c.push(10)
        c.push(5)
        self.assertEqual(c.minus(), 5)
        c.push(10)
        c.push(5)
        self.assertEqual(c.mul(), 50)
        c.push(10)
        c.push(5)
        self.assertEqual(c.div(), 2)
        c.push(10)
        c.dup()
        c.push(5)
        self.assertEqual(c.div(), 2)
        self.assertEqual(c.div(), 5)
    def test_exec(self):
        c = rpn.calc()
        c.exec("3")
        c.exec("3.14")
        self.assertEqual(c.stack, [3, 3.14])
        c.clear()
        c.exec("0x10")
        c.exec(".1e2")
        with self.assertRaises(KeyError): c.exec("gurka")
        self.assertEqual(c.stack, [16, 10.0])
        self.assertEqual(c.exec("+"), 26)
    def test_eval(self):
        c = rpn.calc()
        self.assertEqual(c.eval("2 5 +"), 7)
        self.assertEqual(c.eval("c"), None)
        self.assertEqual(c.eval("2 sq sqrt"), 2)
        self.assertAlmostEqual(c.eval("2 sq pi *"), 12.56, delta=0.5)
if __name__ == '__main__':
    unittest.main()
