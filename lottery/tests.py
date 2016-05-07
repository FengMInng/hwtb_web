from django.test import TestCase

# Create your tests here.


class LotterTestCase(TestCase):
    def setUp(self):
        TestCase.setUp(self)
    
    
    def test_guess_dlt(self):
        