# Django REST API

## Описание проекта
Этот проект представляет собой Django REST API для управления собаками и породами. Он позволяет пользователям выполнять CRUD-операции (создание, чтение, обновление и удаление) над моделями "Порода" и "Собака". Аутентификация пользователей осуществляется с помощью JWT-токенов.


---

## Установка и запуск проекта
### Шаг 1: Создайте файл `.env`
Добавьте переменные окружения в файл `.env`:
```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
```

### Шаг 2: Соберите и запустите контейнеры с помощью Docker
```bash
docker-compose up --build
```
Это создаст и запустит контейнеры для Django-приложения и базы данных PostgreSQL.

---

## API Endpoints
| Метод   | URL               | Описание                          |
|---------|-------------------|-----------------------------------|
| POST    | /api/token/       | Получение JWT-токена              |
| POST    | /api/token/refresh/ | Обновление JWT-токена            |
| GET     | /api/breeds/      | Получение списка пород            |
| POST    | /api/breeds/      | Добавление новой породы           |
| GET     | /api/dogs/        | Получение списка собак            |
| POST    | /api/dogs/        | Добавление новой собаки           |
| GET     | /api/breeds/{id}/ | Получение информации о породе     |
| PUT     | /api/breeds/{id}/ | Обновление информации о породе    |
| DELETE  | /api/breeds/{id}/ | Удаление породы                   |
| GET     | /api/dogs/{id}/   | Получение информации о собаке     |
| PUT     | /api/dogs/{id}/   | Обновление информации о собаке    |
| DELETE  | /api/dogs/{id}/   | Удаление собаки                   |

### Примеры запросов
#### Получение списка пород (GET)
```
GET /api/breeds/
Authorization: Bearer <your_token>
```
Ответ:
```json
[
  {
    "id": 1,
    "name": "Labrador",
    "size": "large",
    "friendliness": 5,
    "trainability": 4,
    "shedding_amount": 3,
    "exercise_needs": 5
  }
]
```

#### Добавление новой породы (POST)
```
POST /api/breeds/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "name": "Beagle",
  "size": "medium",
  "friendliness": 4,
  "trainability": 3,
  "shedding_amount": 2,
  "exercise_needs": 4
}
```
Ответ:
```json
{
  "id": 2,
  "name": "Beagle",
  "size": "medium",
  "friendliness": 4,
  "trainability": 3,
  "shedding_amount": 2,
  "exercise_needs": 4
}
```

#### Удаление собаки (DELETE)
```
DELETE /api/dogs/1/
Authorization: Bearer <your_token>
```
Ответ:
```
HTTP 204 No Content
```

---

## Модели
### Breed
Модель для описания породы собак:
- `name` (CharField): Название породы
- `size` (CharField): Размер породы (tiny, small, medium, large)
- `friendliness` (PositiveSmallIntegerField): Дружелюбие
- `trainability` (PositiveSmallIntegerField): Обучаемость
- `shedding_amount` (PositiveSmallIntegerField): Количество линьки
- `exercise_needs` (PositiveSmallIntegerField): Потребность в активности

### Dog
Модель для описания собаки:
- `name` (CharField): Имя собаки
- `age` (PositiveSmallIntegerField): Возраст собаки
- `breed` (ForeignKey): Порода собаки
- `gender` (CharField): Пол
- `color` (CharField): Цвет
- `favorite_food` (CharField): Любимая еда
- `favorite_toy` (CharField): Любимая игрушка
- `owner` (ForeignKey): Хозяин собаки

---

## Вьюсеты
### BreedViewSet
Вьюсет для управления породами:
- Позволяет выполнять операции получения списка пород, добавления, обновления и удаления.
- При запросе списка пород добавляет аннотацию количества собак для каждой породы.

### DogViewSet
Вьюсет для управления собаками:
- Позволяет выполнять операции получения списка собак, добавления, обновления и удаления.
- При запросе списка собак аннотирует каждую собаку средним возрастом собак той же породы.
- При запросе конкретной собаки аннотирует её количеством собак той же породы.

---

## URL Configuration
Файл `urls.py` в приложении API содержит следующие маршруты:
```python
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .views import BreedViewSet, DogViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('breeds', BreedViewSet, basename='breeds')
router.register('dogs', DogViewSet, basename='dogs')

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
```

---

