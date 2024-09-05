""" В этом модуле хранятся основные классы, которые наследуются различными
контроллерами. Например, здесь хранятся логики сохранения состояния реле или
дискретных выводов, изменения состояний и тд"""

from abc import ABC, abstractmethod
import datetime


class ControllerSoftDict(ABC):
    spec_addr = {}
    my_dict = {}
    map_keys_amount: int = None
    starts_with: int = 0

    def init_dict(self):
        """ Создаем словарь, где ключом будет номер канала,
        а значением: еще один словарь с информацией о канале (состояние и тд)

        :return {0: {'state': None, "changed": datetime.datetime.now()},
        1: {...}, ...}"""
        points_dict = {}
        for i in range(self.map_keys_amount):
            # Начинаем генерировать, первое значение - 0
            if self.starts_with:  # Если номер первого канала на контроллере > 0
                i += self.starts_with  # Плюсуем номер
            # Если вдруг канал не соответстует адресу, его нужно заранее указать
            # в spec_addr, ибо по умолчанию в словаре addr=channel
            if i in self.spec_addr.keys():
                addr = self.spec_addr[i]
            else:
                addr = i
            points_dict[i] = {"state": None,
                              "changed": None,
                              "addr": addr}
        self.my_dict = points_dict
        return points_dict

    def set_point_state_in_dict(self, num, state, changed: bool = True):
        """ Программно задать состояние реле"""
        if changed:
            changed = datetime.datetime.now()
        for chanel, info in self.my_dict.items():
            if info["addr"] == num:
                info["state"] = state
                info["changed"] = changed
        # self.my_dict[num]["state"] = state
        # self.my_dict[num]["changed"] = changed

    def get_dict(self):
        return self.my_dict

    def get_point_state(self, num):
        if num not in self.my_dict:
            return {"error": f"Point num ({num}) not found in dict "
                             f"({self.my_dict})"}
        return self.my_dict[num]


class ControllerPhysOperator(ABC):
    """ В этом классе задаются функции для реального
    взаимодействия с контроллером. На новых контроллерах нужно будет менять
    (предопределять только эти методы),
    потому что вся остальная логика меняться не должна,
    меняются только способ и вид взаимодействия с контроллерами"""
    ip = None
    port = None

    @abstractmethod
    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        return {}


class ControllerPhysRelayOperator(ControllerPhysOperator, ABC):
    @abstractmethod
    def change_phys_relay_state(self, addr, state: bool):
        """ Физически изменить состояние реле (обратиться к контроллеру) """
        return


class ControllerInterface(ControllerSoftDict, ControllerPhysOperator, ABC):
    """ Интерфейс для работы с контроллером.
    В нем происходят работы и со словарем состояний и с реальными состояниями
    физического контроллера """
    name = None

    def __init__(self, controller):
        self.controller = controller
        self.init_dict()

    def update_dict(self):
        phys_relays_map = self.get_phys_dict()
        if not self.my_dict:
            return {"error": "Init relays map (init_relays_map) first!"}
        for addr, state in phys_relays_map.items():
            # relay += self.starts_with
            self.set_point_state_in_dict(addr, state, changed=False)


class RelayControllerInterface(ControllerPhysRelayOperator,
                               ControllerInterface, ABC):
    def change_relay_state(self, num: int, state: bool):
        """ Изменить состояние реле"""
        num = int(num)
        self.set_point_state_in_dict(num, state)
        if num in self.spec_addr.keys():
            num = self.spec_addr["addr"]
        return self.change_phys_relay_state(num, state)
