<h1>friends-service</h1>
Сервис для добавления людей в друзья.
OpenAPI-схема: [friends_service/openapi-schema.yml](friends_service/openapi-schema.yml))

<h3>Запуск</h3>

```
docker build -t friends .
docker run -p 8000:8000 friends
```

<h3>Использование</h3>

Для начала нужно зарегистрироваться:

```
POST /auth/register
username: egor
password: 1387
```

и залогиниться:

```
POST /auth/token/login
username: egor
password: 1387
```
(этот запрос вернет токен, его нужно будет передавать в заголовке во всех дальнейших запросах: `{"Authorization": f"Token {token}"}`))

Краткое описание методов API (более полное смотри в [friends_service/openapi-schema.yml](friends_service/openapi-schema.yml)):

Все запросы начинаются с ```/api/v1```.

`GET /friends/requests/incoming` - входящие заявки в друзья

`GET /friends/requests/outgoing` - исходящие заявки в друзья

`POST /friends/requests/send` - отправить заявку в друзья (в теле передается `{id: <id пользователя, котому отправим заявку}`). Если два человека отправили друг другу заявки, то они сразу станут друзьями.

`POST /friends/requests/accept` - принять заявку в друзья (в теле передается `{id: <id пользователя, который отправил заявку}`)

`POST /friends/requests/decline` - принять заявку в друзья (в теле передается `{id: <id пользователя, который отправил заявку}`)

`GET /friends/all` - получить список друзей

`GET /friends/check_status` - узнать статус человека по id

`GET /friends/delete` - удалить друга по id


<h3>Схема базы</h3>
`User` - стандартная модель из Django

`FriendshipRequest` - запросы на дружбу. Поля: `from_user`, `to_user` - внешние ключи на User'ов

`Friendship` - друзья. Поля: `friend_1`, `friend_2` - внешние ключи на User'ов

