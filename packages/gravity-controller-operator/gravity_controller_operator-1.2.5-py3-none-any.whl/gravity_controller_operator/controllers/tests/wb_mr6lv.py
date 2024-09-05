import unittest
from gravity_controller_operator.controllers.wb_mr6lv import WBMR6LV


class TestCase(unittest.TestCase):
    controller = WBMR6LV("COM11", 144)


if __name__ == "__main__":
    unittest.main()