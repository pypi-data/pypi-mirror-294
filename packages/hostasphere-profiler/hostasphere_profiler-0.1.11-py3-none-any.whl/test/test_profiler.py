import unittest
from time import sleep

from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051',
    token='hsp_514ff0e682f285e2320fc7e6e161557344f154e73ac4bb4d122f959c938e6e6b'
)


class TestProfiler(unittest.TestCase):
    @profiler.track()
    def sample_function(self, start, end):
        sleep(1)
        return sum(range(start, end))

    def test_sample_function(self):
        result = self.sample_function(1, 1000)
        self.assertEqual(result, sum(range(1000)))


if __name__ == '__main__':
    unittest.main()
    # profiler.stop()
