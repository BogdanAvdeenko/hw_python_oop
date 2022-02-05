from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # Для перевода значений из м в км.
    MIN_IN_H: int = 60  # Для перевода часов в минуты.
    LEN_STEP: float = 0.65  # Расстояние за один шаг.

    def __init__(self,
                 action: int,  # Действие во время тренировки;
                 duration: float,  # Длительность тренировки;
                 weight: float  # Вес;
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (
            self.action * self.LEN_STEP / Training.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.get_distance() / self.duration_h
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUNNING_BURN_UP: int = 18  # Параметр расхода калорий при беге №1.
    RUNNING_BURN_OUT: int = 20  # Параметр расхода калорий при беге №2.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (self.RUNNING_BURN_UP * self.get_mean_speed()
             - self.RUNNING_BURN_OUT)
            * self.weight_kg / Training.M_IN_KM
            * self.duration_h * Training.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALKING_BURN_UP: float = 0.035  # Параметр расхода калорий при ходьбе №1.
    WALKING_BURN_OUT: float = 0.029  # Параметр расхода калорий при ходьбе №2.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (
            (self.WALKING_BURN_UP * self.weight_kg
             + (self.get_mean_speed() ** 2 // self.height)
             * self.WALKING_BURN_OUT * self.weight_kg)
            * self.duration_h * Training.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Расстояние за один гребок.
    SWIMMING_BURN_UP: float = 1.1  # Параметр расхода калорий при плаваньи №1.
    SWIMMING_BURN_OUT: int = 2  # Параметр расхода калорий при плаваньи №2.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # Длина бассейна.
        self.count_pool = count_pool  # Количество проплытых бассейнов.

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плаванья."""
        return (
            self.length_pool * self.count_pool
            / Training.M_IN_KM / self.duration_h
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плаваньи."""
        return (
            (self.get_mean_speed() + self.SWIMMING_BURN_UP)
            * self.SWIMMING_BURN_OUT * self.weight_kg
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
