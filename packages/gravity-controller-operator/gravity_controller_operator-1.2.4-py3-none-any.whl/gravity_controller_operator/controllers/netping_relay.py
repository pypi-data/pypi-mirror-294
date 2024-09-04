import netping_contr.main

from gravity_controller_operator.controllers_super import ControllerInterface, \
    RelayControllerInterface


class NetPing2ControllerDI(ControllerInterface):
    map_keys_amount = 4
    starts_with = 1

    def __init__(self, controller):
        super(NetPing2ControllerDI, self).__init__(controller)
        self.update_dict()

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        response_raw = self.controller.get_all_di_status()
        response_parsed = self.controller.parse_all_lines_request(
            response_raw)
        return response_parsed


class NetPing2ControllerRelay(RelayControllerInterface):
    map_keys_amount = 4
    starts_with = 1
    controller = None

    def __init__(self, controller):
        super().__init__(controller)
        self.update_dict()

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        response_parsed = self.controller.get_all_relay_states()
        return response_parsed

    def change_phys_relay_state(self, num, state: bool):
        response = self.controller.change_relay_status(relay_num=num,
                                                       status=state)
        while "error" in response:
            response = self.controller.change_relay_status(
                relay_num=num, status=state)


class NetPing2Controller:
    model = "netping_relay"

    def __init__(self, ip, port=80, username="visor", password="ping",
                 name="netping_relay2", *args, **kwargs):
        self.controller_interface = netping_contr.main.NetPingDevice(
            ip=ip,
            port=port,
            username=username,
            password=password
        )
        self.relay_interface = NetPing2ControllerRelay(
            self.controller_interface)
        self.di_interface = NetPing2ControllerDI(
            self.controller_interface)
