from django.db.models import Avg, OuterRef, Subquery, Count
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from api.permissions import ReadOrAuthenticated, ReadOrAuthenticatedOrOwner
from backend.api.serializers import BreedSerializer, DogSerializer
from dogs.models import Breed, Dog


class BreedViewSet(viewsets.ModelViewSet):
    """Вьюсет получения/добавления/обновления/удаления 'Breed'."""

    serializer_class = BreedSerializer
    permission_classes = (ReadOrAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        """
        Возвращает queryset пород собак с аннотацией количества собак
        для каждой породы.

        Если выполняется действие 'list', добавляется количество собак для каждой породы.

        Возвращает:
            QuerySet: queryset пород собак, возможно с аннотацией количества собак.
        """
        if self.action == 'list':
            subquery = (
                Dog.objects.filter(breed=OuterRef('pk'))
                .values('breed')
                .annotate(count=Count('id'))
                .values('count')
            )
            return Breed.objects.annotate(dog_count=Subquery(subquery))

        return Breed.objects.all()


class DogViewSet(viewsets.ModelViewSet):
    """
    ViewSet для получения, создания, обновления и удаления 'Dog'.

    Этот ViewSet позволяет управлять собаками, включая:
    - Получение списка всех собак с указанием среднего возраста собак каждой породы.
    - Получение подробной информации о конкретной собаке, включая количество собак той же породы.
    """

    serializer_class = DogSerializer
    permission_classes = (ReadOrAuthenticatedOrOwner,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        """
        Возвращает queryset собак с дополнительными аннотациями в зависимости от действия.

        - Для действия 'list': аннотирует каждую собаку средним возрастом собак той же породы.
        - Для действия 'retrieve': аннотирует каждую собаку количеством собак той же породы.

        Возвращает:
            QuerySet: queryset собак, возможно аннотированный средним возрастом или количеством собак той же породы.
        """
        if self.action == 'list':
            avg_age_subquery = (
                Dog.objects.filter(breed=OuterRef('breed'))
                .values('breed')
                .annotate(avg_age=Avg('age'))
                .values('avg_age')[:1]
            )
            return Dog.objects.annotate(avg_age=Subquery(avg_age_subquery))

        if self.action == 'retrieve':
            same_breed_count_subquery = (
                Dog.objects.filter(breed=OuterRef('breed'))
                .values('breed')
                .annotate(count=Count('id'))
                .values('count')[:1]
            )
            return Dog.objects.annotate(
                same_breed_count=Subquery(same_breed_count_subquery)
            )

        return Dog.objects.all()
