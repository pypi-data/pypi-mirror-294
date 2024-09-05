import threading
import time
from _thread import allocate_lock
from gravity_controller_operator.controllers.arm_k210 import ARMK210Controller
from gravity_controller_operator.controllers.wb_mr6lv import WBMR6LV
from gravity_controller_operator.controllers.netping_relay import NetPing2Controller
from gravity_controller_operator.controllers.emulator_contr import EmulatorController

AVAILABLE_CONTROLLERS = [ARMK210Controller, WBMR6LV, NetPing2Controller,
                         EmulatorController]


class ControllerCreater:
    @staticmethod
    def get_controller(model, emulator, *args, **kwargs):
        for contr in AVAILABLE_CONTROLLERS:
            if emulator:
                inst = EmulatorController(*args, **kwargs)
                return inst
            if contr.model == model:
                inst = contr(*args, **kwargs)
                return inst
        raise UnknownController


class ControllerOperator:
    """ Класс для работы с ПЛК контроллерами.
    Предоставляет собой единый интерфейс для работы с различными контроллерами.
    Контроллеры необходимо создавать в директории controllers """

    def __init__(self, controller_inst, auto_update_points: bool = False,
                 update_cooldown=0.25, name="unknown"):
        self.mutex = allocate_lock()
        self.update_cooldown = update_cooldown
        self.controller = controller_inst
        self.di_interface = self.init_di_interface()
        self.relay_interface = self.init_relay_interface()
        self.points = {}
        self.update_points()
        if auto_update_points:
            threading.Thread(
                target=self.auto_update_points, daemon=True).start()

    def auto_update_points(self, frequency=0):
        while True:
            self.update_points()
            time.sleep(frequency)

    def change_relay_state(self, num, state):
        self.mutex.acquire()
        self.relay_interface.change_relay_state(num, state)
        self.mutex.release()

    def update_points(self):
        self.mutex.acquire()
        if self.di_interface:
            self.di_interface.update_dict()
            self.points["di"] = self.di_interface.get_dict()
        if self.relay_interface:
            self.relay_interface.update_dict()
            self.points["relays"] = self.relay_interface.get_dict()
        self.mutex.release()
        time.sleep(self.update_cooldown)

    def init_di_interface(self):
        di_interface = self.controller.di_interface
        return di_interface

    def init_relay_interface(self):
        try:
            relay_interface = self.controller.relay_interface
        except AttributeError:
            relay_interface = None
        return relay_interface

    def get_points(self):
        while not self.points:
            pass
        return self.points


class UnknownController(Exception):
    # Исключение, возникающее при неизвестном имени терминала
    def __init__(self):
        text = 'Такой контроллер не обнаружен! Создайте класс с контроллером ' \
               'в директории controllers, укажите его модель через атрибут ' \
               'model, затем добавьте этот класс в список ' \
               'AVAILABLE_CONTROLLERS'
        super().__init__(text)
