"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет
проверяться доступность сетевых узлов. Аргументом функции является список,
в котором каждый сетевой узел должен быть представлен именем хоста или
ip-адресом. В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения («Узел доступен»,
«Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться
с помощью функции ip_address(). (Внимание! Аргументом сабпроцеса должен
быть список, а не строка!!! Крайне желательно использование потоков.)


------------------ (факультативно) --------------------------

4. *Продолжаем работать над проектом «Мессенджер»:
a) Реализовать скрипт, запускающий два клиентских приложения:
на чтение чата и на запись в него. Уместно использовать модуль subprocess).
b) Реализовать скрипт, запускающий указанное количество клиентских приложений.

5. *В следующем уроке мы будем изучать дескрипторы и метаклассы.
Но вы уже сейчас можете перевести часть кода из функционального стиля в
объектно-ориентированный. Создайте классы «Клиент» и «Сервер»,
а используемые функции превратите в методы классов.
"""
import ipaddress
import os
import platform
import subprocess
import time
import threading
from ipaddress import ip_address
from pprint import pprint
from typing import Optional

endpoints = {
    'available': '',
    'not_available': '',
}


def check_ip_address(value: str) -> ipaddress.IPv4Address:
    try:
        return ip_address(value)
    except ValueError:
        raise ValueError('Incorrect ip address')


def ping(ipv4: ipaddress.IPv4Address, result: dict, get_list: bool) -> str:
    param = '-c'
    response = subprocess.Popen(
        ['ping', param, '1', '-w', '1', str(ipv4)],
        stdout=subprocess.PIPE,
    )
    if response.wait() == 0:
        result['available'] += f'{ipv4}\n'
        res = f"{ipv4} - node available"
    else:
        result['not_available'] += f'{ipv4}\n'
        res = f"{ipv4} - node not available"

    if not get_list:
        print(res)

    return res


def host_ping(hosts: list, get_list=False) -> Optional[dict]:
    threads = []
    for host in hosts:
        ipv4 = host
        try:
            ipv4 = check_ip_address(host)
        except ValueError as e:
            print(f'{host} - {e} воспринимаю как доменное имя')

        thread = threading.Thread(
            target=ping,
            args=(ipv4, endpoints, get_list),
            daemon=True,
        )
        thread.start()
        threads.append(thread)
        for thread in threads:
            thread.join()

    return endpoints if get_list else None


if __name__ == '__main__':
    hosts = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com',
             '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5',
             '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '0.0.1.0']
    start = time.time()
    host_ping(hosts)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(endpoints)

