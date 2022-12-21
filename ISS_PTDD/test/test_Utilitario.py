"""
1 - Escribir las pruebas correspondientes al programa Utilitario
1.1 - Ejecutar las pruebas las cuales deben fallar
2 - Escribir la funcionalidad del programa Utilitario
2.1 - Ejecutar las pruebas las cuales ahora deben pasar
"""
from src import Utilitario as util


def test_is_Prime():
    num = util.is_Prime(19)
    assert num == True


def test_gelOld():
    old = util.getOld('2003-01-01')
    assert old == 17


def test_netSal():
    net_salary = util.netSal(30000)
    assert net_salary == 21170.25
