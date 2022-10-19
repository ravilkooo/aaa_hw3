import json


class JSONConveter:
    # Класс, которыё преобразовывает JSON-данные в python-словарь
    def convert_to_dict(self, json_data):
        # Разбираем поля объявления и переводим их в словарь
        python_dict = json.loads(json_data)
        return python_dict


class Location:
    # Класс, который позволяет хранить данные о местоположени,
    # которые будут являтся аттрибутами экземпляров этого класса
    def __init__(self, attr_dict):
        for key, value in attr_dict.items():
            self.__dict__[key] = value


class ColorizeMixin:
    def __init__(self):
        self.repr_color_code = 33

    def __repr__(self):
        return f'\033[{self.repr_color_code}m{self.title}' \
               f' | {self.price} ₽\033[0m'


class Advert(ColorizeMixin):
    def __init__(self, attr_dict):
        # Проверяем наличие обязательного аттрибута title
        if 'title' not in attr_dict:
            raise AttributeError('Advert object must have "title" attribute.')

        # Проверяем наличие аттрибута price и его корректность при наличии
        if 'price' not in attr_dict:
            self.__dict__['_price'] = 0
        elif attr_dict['price'] < 0:
            raise ValueError('price must be >= 0 ')
        else:
            self.__dict__['_price'] = attr_dict['price']
            del attr_dict['price']

        # Динамически создаём аттрибуты и присваиваем значения
        for key, value in attr_dict.items():
            self.__dict__[key] = value

        # При наличии поля location создаём объект, к аттрибутам которого
        # можно будет обращаться через точку (например loaction.address)
        if 'location' in attr_dict:
            self.location = Location(self.location)

        # Вызываем конструктор миксина
        super().__init__()

    @property
    def price(self):
        return self._price


def test1():
    python_str = """{
        "title": "python", "price": 0,
        "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
        }"""
    conv = JSONConveter()
    python_data = conv.convert_to_dict(python_str)
    python_adv = Advert(python_data)
    print(python_adv)
    print(f'Адрес {python_adv.title} : {python_adv.location.address}')
    print(f'Стоимоcть {python_adv.title} : {python_adv.price}')

    corgi_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
        }"""
    corgi_data = conv.convert_to_dict(corgi_str)
    corgi_adv = Advert(corgi_data)
    print(corgi_adv)
    print(f'Адрес {corgi_adv.title} : {corgi_adv.location.address}')
    print(f'Стоимоcть {corgi_adv.title} : {corgi_adv.price}')


if __name__ == '__main__':
    test1()
