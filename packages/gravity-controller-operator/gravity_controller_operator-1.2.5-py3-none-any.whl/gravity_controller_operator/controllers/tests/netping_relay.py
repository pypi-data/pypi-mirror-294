from gravity_controller_operator.controllers.netping_relay import \
    NetPing2Controller
import unittest


class TestCase(unittest.TestCase):
    controller = NetPing2Controller(ip="192.168.0.100")

    def test_di(self):
        self.controller.di_interface.update_dict()
        res = self.controller.di_interface.get_dict()
        print(res)
        res = self.controller.relay_interface.get_dict()
        print(res)

if __name__ == "__main__":
    unittest.main()