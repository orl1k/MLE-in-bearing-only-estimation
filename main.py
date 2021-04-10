import numpy as np
from lib.object import Object
from lib.tests import Tests
from lib.model import Model

# Пример моделирования

# Создаем наблюдатель
observer_x, observer_y, observer_course, observer_velocity = 0.0, 0.0, 0.0, 5.0
observer = Object(
    "Наблюдатель",
    observer_x,
    observer_y,
    observer_course,
    observer_velocity,
    verbose=True,
)
# Создаем объект
target_bearing, target_distance, target_course, target_velocity = (
    0.0,
    20.0,
    45.0,
    10.0,
)

target = Object(
    "Объект",
    target_bearing,
    target_distance,
    target_course,
    target_velocity,
    observer,
    mode="bdcv",
    verbose=True,
)

# Моделирование траекторий
observer.forward_movement(3 * 60)
observer.change_course(270, "left", omega=0.5)
observer.forward_movement(5 * 60)
observer.change_course(90, "right", omega=0.5)
observer.forward_movement(3 * 60)

# Время движения объекта должно совпадать с временем наблюдателя для TMA
target.forward_movement(len(observer.coords[0]) - 1)

import pandas as pd

p0 = [0.0, 25.0, 90.0, 7.0]
d_arr = [10.0, 20.0, 30.0, 40.0]
std_arr = [0.0, 0.1, 0.2, 0.3, 0.5, 1.0]


def target_func(seed=None):
    rng = np.random.RandomState(seed)
    b = 0
    d = rng.uniform(5, 50)
    c = rng.uniform(0, 180)
    v = rng.uniform(3, 15)
    return [b, d, c, v]


from lib.algorithms import mle_algorithm_v2, dynamic_mle
from lib.algorithms import swarm
from lib.functions import get_df


model = Model(observer)
model.noise_std = np.radians(0.0)
dict_results = swarm(
    model,
    algorithm_name="ММП в реальном времени",
    n=2,
    target_func=target_func,
    p0=p0,
    seeded=True,
)
df = get_df(dict_results)
print(df.round(1).iloc[0::3, :].head())

# model = Model(observer, end_t=420)
# model.noise_std = np.radians(0.0)
# dict_results = swarm(
#     model,
#     algorithm_name="ММП",
#     n=5,
#     target_func=target_func,
#     p0=p0,
#     seeded=True,
# )
# df = get_df(dict_results)
# print(df.round(1).head())

# # Рассматривается маневр объекта
# target.forward_movement(7 * 60)
# target.change_course(270, "left", omega=0.5)
# target.forward_movement(len(observer.coords[0]) - len(target.coords[0]))

# # Запуск множества моделей
# dict_results = tma.swarm(n=100, fixed_target=False, fixed_noise=False, p0=[0., 20., 45., 10.])
# df = f.get_df(dict_results)
# tests.save_df(df)
