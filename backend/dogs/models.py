from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from backend.core.constants import MAX_VALUE_ABILITIES, MIN_VALUE_ABILITIES


User = get_user_model()


class Breed(models.Model):
    """Модель 'Порода'."""

    class BreedSizes(models.TextChoices):
        """Размеры породы."""

        TINY = 'tiny'
        SMALL = 'small'
        MEDIUM = 'medium'
        LARGE = 'large'

    name = models.CharField(verbose_name='Название')
    size = models.CharField(choices=BreedSizes.choices, verbose_name='Размер')
    friendliness = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE_ABILITIES),
            MaxValueValidator(MAX_VALUE_ABILITIES),
        ],
        verbose_name='Дружелюбие',
    )
    trainability = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE_ABILITIES),
            MaxValueValidator(MAX_VALUE_ABILITIES),
        ],
        verbose_name='Обучаемость',
    )
    shedding_amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE_ABILITIES),
            MaxValueValidator(MAX_VALUE_ABILITIES),
        ],
        verbose_name='Количество линьки',
    )
    exercise_needs = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE_ABILITIES),
            MaxValueValidator(MAX_VALUE_ABILITIES),
        ],
        verbose_name='Потребность в активности',
    )

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ('name',)


class Dog(models.Model):
    """Модель 'Собака'."""

    name = models.CharField(verbose_name='Имя')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        null=True,
        related_name='dogs',
        verbose_name='Порода',
    )
    gender = models.CharField(verbose_name='Пол')
    color = models.CharField(verbose_name='Цвет')
    favorite_food = models.CharField(null=True, verbose_name='Любимая еда')
    favorite_toy = models.CharField(null=True, verbose_name='Любимая игрушка')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name='Хозяин собаки',
    )

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
        ordering = ('name',)
