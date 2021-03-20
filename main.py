import numpy as np
from ship import Ship
from tests import Tests
from botma import TMA
import lm
import time

# Класс для сохранения результатов
tests = Tests('1')

# Пример моделирования

# Создаем наблюдатель
observer_x, observer_y, observer_course, observer_velocity = 0, 0, 0, 3
observer = Ship('Наблюдатель', observer_x, observer_y, observer_course,
                observer_velocity, verbose=True)
# Создаем объект
target_bearing, target_distance, target_course, target_velocity = 0, 20, 45, 10
target = Ship('Объект', target_bearing, target_distance, target_course,
              target_velocity, observer, mode='bdcv', verbose=True)

# Моделирование траекторий
observer.forward_movement(3 * 60)
observer.change_course(270, 'left', omega=0.5)
observer.forward_movement(2 * 60)
observer.change_course(90, 'right', omega=0.5)
observer.forward_movement(5 * 60)

# Время движения объекта должно совпадать с временем наблюдателя для TMA
target.forward_movement(len(observer.coords[0])-1)

# # Рассматривается маневр объекта
# target.forward_movement(10 * 60)
# target.change_course(270, 'left', omega=0.5)
# target.forward_movement(360)

tma = TMA(observer, target, sd=np.radians(0.5), seed=1)
tma.print_verbose()

print(tma.mle_algorithm_v6([1,1,1,1]))
tma.get_observed_information()

# r = tma.swarm(5)
# tests.save_results(r)

# tma.set_target(p0=tma.get_random_p0())
# p0 = tma.get_random_p0(seed = 692 + 1000)
# p0[0] = Ship.transform_to_angle(np.radians(p0[0]))
# p0[2] = Ship.transform_to_angle(np.radians(p0[2]))
# b, d, c, v = p0
# p0 = [d * np.cos(b), d * np.sin(b), v * np.cos(c), v * np.sin(c)]
# tma.mle_algorithm_v6(p0)

# # Запуск множества моделей
# r = tma.swarm(100)
# tests.save_results(r)
