import netping_contr.main

from gravity_controller_operator.controllers_super import ControllerInterface, \
    RelayControllerInterface


class EmulatorDI(ControllerInterface):
    map_keys_amount = 4
    starts_with = 1

    def __init__(self, controller):
        super(EmulatorDI, self).__init__(controller)
        self.update_dict()

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        return {1:0, 2:0, 3:0, 4:0}


class EmulatorRelay(RelayControllerInterface):
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
        return {1: 0, 2: 0, 3: 0, 4: 0}

    def change_phys_relay_state(self, num, state: bool):
        pass


class EmulatorController:
    model = "emulator_controller"

    def __init__(self, ip, port=80, username="visor", password="ping",
                 name="netping_relay2", *args, **kwargs):
        self.relay_interface = EmulatorRelay(None)
        self.di_interface = EmulatorDI(None)
