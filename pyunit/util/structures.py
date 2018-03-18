# $Revision: 1.1 $

from genetics.util.structures import Queue
import unittest


class QueueTest(unittest.TestCase):
    '''
    Tests the unsynchronized queue
    '''
    def testQueue(self):
        q = Queue([1])
        self.assertTrue(not q.empty())
        self.assertEqual(q.dequeue(), 1)
        self.assertTrue(q.empty())
        self.assertRaises(IndexError, q.dequeue)
        q.enqueue(2)
        self.assertTrue(not q.empty())
        self.assertEqual(q.dequeue(), 2)
        self.assertTrue(q.empty())
        
            
if __name__ == '__main__':
    unittest.main()