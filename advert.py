import json


class JSONConveter:
    # Класс, которыё преобразовывает JSON-данные в python-словарь
    def convert_to_dict(self, json_data):
        # Разбираем поля объявления и переводим их в словарь
        python_dict = json.loads(json_data)
        return python_dict


class Attributable:
    # Класс, который позволяет хранить данные о местоположени,
    # которые будут являтся аттрибутами экземпляров этого класса
    def __init__(self, attr_dict):
        for key, value in attr_dict.items():
            if type(value) is dict:
                self.__dict__[key] = Attributable(value)
            else:
                self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)


class ColorizeMixin:
    def __init__(self):
        self.repr_color_code = 33

    def __str__(self):
        # return f'\033[{self.repr_color_code}m{self.title} | {self.price} ₽\033[0m'
        return f'\033[{self.repr_color_code}m{self.__repr__()}\033[0m'


class Advert(ColorizeMixin):
    def __init__(self, attr_dict):
        # Проверяем наличие обязательного аттрибута title
        if 'title' not in attr_dict:
            print('Advert object must have "title" attribute.')
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
            if type(value) is dict:
                self.__dict__[key] = Attributable(value)
            else:
                self.__dict__[key] = value

        # Вызываем конструктор миксина
        super().__init__()

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        assert new_price > 0, 'price must be >= 0 '
        self._price = new_price


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
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25",
        "index" : 253120
        }
        }"""
    corgi_data = conv.convert_to_dict(corgi_str)
    corgi_adv = Advert(corgi_data)
    print(corgi_adv.location)
    print(f'Адрес {corgi_adv.title} : {corgi_adv.location.address}')
    print(f'Стоимоcть {corgi_adv.title} : {corgi_adv.price}')

    try:
        Advert({"class": "value"})
    except AttributeError as e:
        print(f'Got an AttributeError: {e}')


if __name__ == '__main__':
    test1()
