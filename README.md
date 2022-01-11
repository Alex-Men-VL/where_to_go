# Куда пойти — Москва глазами Артёма

Сайт с картой с интересными местами в Москве. На карте отображается маркеры, кликнув
по которым, можно получить полное описание места с фотографиями и полезными ссылками.

![Демка сайта](.gitbook/assets/site.png)

[Демка сайта](http://almen.pythonanywhere.com/).

## Как запустить

Скачайте код
```bash
$ git clone https://github.com/Alex-Men-VL/where_to_go.git
$ cd where_to_go
```
Установите зависимости:
```bash
$ pip install -r requirements.txt
```
Накатите миграцию:
```bash
$ python3 manage.py migrate
```
Запустите сервер:
```bash
$ python3 manage.py runserver
```

Чтобы открыть локальную версию сайта, перейдите по адресу `http://127.0.0.1:8000/`

## Переменные окружения

Часть данных берется из переменных окружения. Чтобы их определить, создайте файл 
`.env` рядом с `manage.py` и запишите туда данные в таком формате: 
`ПЕРЕМЕННАЯ=значение`

`SECRET_KEY` — секретный ключ Django;

`DEBUG` — режим отладки, по дефолту False;

`DB_ENGINE` - бэкенд вашей базы данных;

`DB_NAME` - имя бд;

## Заполнение бд

### Через панель администратора

- Создайте суперпользователя:
```bash
$ python3 manage.py createsuperuser
```
- Перейдите в админку по адресу `http://127.0.0.1:8000/admin`

### Через консоль

Чтобы загрузить данные в формате JSON, воспользуйтесь следующей командой:
```bash
$ python3 manage.py load_place http://адрес/файла.json
```

Образец JSON файла:

```json
{
    "title": "Антикафе Bizone",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1f09226ae0edf23d20708b4fcc498ffd.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/6e1c15fd7723e04e73985486c441e061.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/be067a44fb19342c562e9ffd815c4215.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/f6148bf3acf5328347f2762a1a674620.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b896253e3b4f092cff47a02885450b5c.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/605da4a5bc8fd9a748526bef3b02120f.jpg"
    ],
    "description_short": "Настольные и компьютерные игры, виртуальная реальность и насыщенная программа мероприятий — новое антикафе Bizone предлагает два уровня удовольствий для вашего уединённого отдыха или радостных встреч с родными, друзьями, коллегами.",
    "description_long": "<p>Рядом со станцией метро «Войковская» открылось антикафе Bizone, в котором создание качественного отдыха стало делом жизни для всей команды. Создатели разделили пространство на две зоны, одна из которых доступна для всех посетителей, вторая — только для совершеннолетних гостей.</p><p>В Bizone вы платите исключительно за время посещения. В стоимость уже включены напитки, сладкие угощения, библиотека комиксов, большая коллекция популярных настольных и видеоигр. Также вы можете арендовать ВИП-зал для большой компании и погрузиться в мир виртуальной реальности с помощью специальных очков от топового производителя.</p><p>В течение недели организаторы проводят разнообразные встречи для меломанов и киноманов. Также можно присоединиться к английскому разговорному клубу или посетить образовательные лекции и мастер-классы. Летом организаторы запускают марафон настольных игр. Каждый день единомышленники собираются, чтобы порубиться в «Мафию», «Имаджинариум», Codenames, «Манчкин», Ticket to ride, «БЭНГ!» или «Колонизаторов». Точное расписание игр ищите в группе антикафе <a class=\"external-link\" href=\"https://vk.com/anticafebizone\" target=\"_blank\">«ВКонтакте»</a>.</p><p>Узнать больше об антикафе Bizone и забронировать стол вы можете <a class=\"external-link\" href=\"http://vbizone.ru/\" target=\"_blank\">на сайте</a> и <a class=\"external-link\" href=\"https://www.instagram.com/anticafe.bi.zone/\" target=\"_blank\">в Instagram</a>.</p>",
    "coordinates": {
        "lng": "37.50169",
        "lat": "55.816591"
    }
}
```

[Тестовые данные](https://github.com/devmanorg/where-to-go-places).

## Используемые библиотеки

* [Leaflet](https://leafletjs.com/) — отрисовка карты
* [loglevel](https://www.npmjs.com/package/loglevel) для логгирования
* [Bootstrap](https://getbootstrap.com/) — CSS библиотека
* [Vue.js](https://ru.vuejs.org/) — реактивные шаблоны на фронтенде

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).
