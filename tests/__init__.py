from dom import *
from dom.extras import CenterText
from bootstraps import BootstrapTemplate

import unittest

class TestBootstrap(unittest.TestCase):
    def setUp(self):
        self.form = Form.from_file("tests/fixtures/checkout.yaml")

    def testCheckoutForm(self):
        header = CenterText()
        header.add(Img("https://getbootstrap.com/docs/5.1/assets/brand/bootstrap-logo.svg", "d-block mx-auto mb-4", width=72, height=57))
        header.add(H2("Checkout form"))
        template = BootstrapTemplate()
        template.body.add(header).add(self.form)


        with open("tests/fixtures/checkout.html", "r") as f:
            expected = f.read()

        self.assertEqual(expected, template.render())

