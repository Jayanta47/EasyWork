from django.test import TestCase

# Create your tests here.
from .utils import cost_month_graph

class CostTestCases(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def testCost(self):
        print(cost_month_graph())