import unittest
import queue
import random

MAX_RAND = 10000

class QueueTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = queue.Queue(5)

    def test_enqueue(self):
        self.assertEqual(len(self.queue.data), 5)
        self.queue.enqueue(1)
        self.assertEqual(self.queue.data, [1]+[None]*4)
        self.assertEqual(self.queue.head, 0)
        self.assertEqual(self.queue.tail, 1)
        self.assertEqual(self.queue.count, 1)
        for i in range(4):
            self.queue.enqueue(i)
        self.assertEqual(self.queue.data, [1,0,1,2,3])
        self.assertEqual(self.queue.head, 0)
        self.assertEqual(self.queue.tail, 0)
        self.assertEqual(self.queue.count, 5)

    def test_dequeue(self):
        self.queue.enqueue(1)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.count, 0)
        r = random.getstate()
        for _ in range(5):
            self.queue.enqueue(random.randrange(MAX_RAND))
        random.setstate(r)
        for _ in range(5):
            self.assertEqual(self.queue.dequeue(), random.randrange(MAX_RAND))
        self.assertEqual(self.queue.count, 0)
        for _ in range(5):
            r = random.getstate()
            for _ in range(3):
                self.queue.enqueue(random.randrange(MAX_RAND))
            r = random.setstate(r)
            for _ in range(3):
                self.assertEqual(self.queue.dequeue(), random.randrange(MAX_RAND))
        self.assertEqual(self.queue.count, 0)

    def test_expand(self):
        for _ in range(4):
            self.queue.enqueue(1)
        self.queue.expand(5) # no-wrap expansion
        self.assertEqual(len(self.queue.data), 10)
        self.assertEqual(self.queue.count, 4)
        self.assertEqual(self.queue.head, 0)
        self.assertEqual(self.queue.tail, 4)
        self.queue.enqueue(1)
        for _ in range(5):
            self.queue.enqueue(2)
        for _ in range(5):
            self.assertEqual(self.queue.dequeue(), 1)
        for _ in range(5):
            self.queue.enqueue(3)
        self.assertEqual(self.queue.head, 5)
        self.assertEqual(self.queue.tail, 5)
        self.assertEqual(self.queue.count, 10)
        for i in range(5):
            self.queue.expand(1) # unwrapping expansions
            self.assertEqual(self.queue.head, 5)
            self.assertEqual(self.queue.tail, 4-i)
            self.assertEqual(len(self.queue.data), 10+i+1)
            self.assertEqual(self.queue.data[10+i], 3)
        self.queue.expand(1) # final unwrap for tail index
        self.assertEqual(self.queue.tail, 15)
        self.assertEqual(self.queue.data[15], None)
        for i in range(5):
            self.assertEqual(self.queue.dequeue(), 2)
        for i in range(5):
            self.assertEqual(self.queue.dequeue(), 3)
        self.assertEqual(self.queue.count, 0)
