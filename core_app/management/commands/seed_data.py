from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core_app.models import Category, City, Ad


CITIES = [
    'Алматы', 'Астана', 'Шымкент', 'Қарағанды', 'Актобе',
    'Тараз', 'Павлодар', 'Өскемен', 'Семей', 'Атырау',
]

CATEGORIES = [
    'Электроника', 'Авто', 'Недвижимость', 'Одежда',
    'Мебель', 'Работа', 'Услуги', 'Животные', 'Спорт', 'Разное',
]

ADS_DATA = [
    {
        'city': 'Алматы', 'category': 'Авто',
        'title': 'Mercedes-Benz GLE 350 2021, AMG пакет',
        'description': 'Продаю Mercedes-Benz GLE 350 2021 года выпуска с AMG пакетом. Цвет Obsidian Black Metallic. Пробег 38 000 км. Один владелец, не такси. Панорамная крыша, вентилируемые и массажные кресла, Burmester аудиосистема, адаптивная подвеска. ПТС чистый.',
        'price': 42000000, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=700&q=80',
    },
    {
        'city': 'Алматы', 'category': 'Недвижимость',
        'title': 'Пентхаус 180 кв.м, ЖК Esentai Tower',
        'description': 'Продается эксклюзивный пентхаус в ЖК Esentai Tower. Площадь 180 кв.м. Дизайнерский ремонт, панорамные окна, вид на горы Заилийского Алатау. Терраса 40 кв.м, умный дом, подземный паркинг на 2 машины. Охрана 24/7.',
        'price': 290000000, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=700&q=80',
    },
    {
        'city': 'Астана', 'category': 'Электроника',
        'title': 'Apple Vision Pro 256GB, полный комплект',
        'description': 'Продаю Apple Vision Pro 256GB. Куплен в США, использовался месяц. Состояние идеальное. Все аксессуары в комплекте: чехол для путешествий, дополнительный аккумулятор, два световых уплотнителя. Гарантия Apple до марта 2025.',
        'price': 980000, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1679678691006-0ad24fecb769?w=700&q=80',
    },
    {
        'city': 'Астана', 'category': 'Авто',
        'title': 'Porsche Cayenne GTS 2022, керамика',
        'description': 'Porsche Cayenne GTS 2022 года. Керамические тормоза, адаптивные амортизаторы PASM, Sport Chrono пакет. Пробег 22 000 км. Interior Edition: кожа цвета Bordeaux Red, карбоновые вставки. Полная история обслуживания в официальном дилере.',
        'price': 68000000, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1550355291-bbee04a92027?w=700&q=80',
    },
    {
        'city': 'Шымкент', 'category': 'Недвижимость',
        'title': 'Дом 350 кв.м с бассейном, Нурсат',
        'description': 'Продается элитный дом в районе Нурсат. Площадь 350 кв.м + участок 8 соток. Открытый бассейн, гостевой домик, баня, летняя кухня. 5 спален, каждая с санузлом. Гараж на 3 машины. Солнечные панели, система умный дом.',
        'price': 180000000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=700&q=80',
    },
    {
        'city': 'Шымкент', 'category': 'Электроника',
        'title': 'DJI Mavic 3 Pro Cine Premium Combo',
        'description': 'Продаю DJI Mavic 3 Pro Cine в комплекте Premium Combo. Тройная камера Hasselblad, съемка ProRes 4K. В наборе 3 аккумулятора, зарядная станция, фильтры ND, чехол. Использовался для коммерческих съемок, налет 14 часов.',
        'price': 720000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?w=700&q=80',
    },
    {
        'city': 'Қарағанды', 'category': 'Работа',
        'title': 'DevOps-инженер в стартап (Senior, remote)',
        'description': 'Ищем Senior DevOps инженера в быстрорастущий fintech стартап. Стек: Kubernetes, Terraform, AWS, GitLab CI. Требования: опыт от 4 лет, сертификация CKA будет плюсом. Зарплата: 700 000 — 1 000 000 тг. Удаленно, гибкий график, опционы.',
        'price': 0, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=700&q=80',
    },
    {
        'city': 'Қарағанды', 'category': 'Спорт',
        'title': 'Беговая дорожка Technogym Run 700',
        'description': 'Беговая дорожка Technogym Run 700 — профессиональное оборудование итальянского производства. Максимальная скорость 22 км/ч, наклон до 15%. Встроенный 10-дюймовый сенсорный экран, WiFi, bluetooth. Пробег 180 км. Причина продажи — переезд.',
        'price': 1200000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=700&q=80',
    },
    {
        'city': 'Актобе', 'category': 'Мебель',
        'title': 'Дизайнерский диван B&B Italia Charles, кожа',
        'description': 'Диван B&B Italia Charles, дизайн Antonio Citterio. Обивка — натуральная кожа Gamma цвета Cognac. Длина 300 см. Куплен в Милане, привезен в 2023 году. Использовался в шоу-руме, состояние как новый. Оригинал с сертификатом.',
        'price': 3800000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=700&q=80',
    },
    {
        'city': 'Актобе', 'category': 'Услуги',
        'title': 'Архитектурное бюро — проекты под ключ',
        'description': 'Профессиональное архитектурное бюро. Разрабатываем проекты частных домов, коммерческих объектов, интерьеров. Авторский надзор, 3D-визуализация, BIM-проектирование. Портфолио — 120+ реализованных объектов. Бесплатная первичная консультация.',
        'price': 0, 'is_top': False,
        'image_url': '',
    },
    {
        'city': 'Тараз', 'category': 'Одежда',
        'title': 'Stone Island Shadow Project, коллекция FW23',
        'description': 'Продаю куртку Stone Island Shadow Project из коллекции FW2023. Размер L. Материал — O-Ventile со специальной мембраной. Куплена в официальном магазине в Милане. Носил 2 раза, состояние идеальное. Архивная вещь.',
        'price': 480000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=700&q=80',
    },
    {
        'city': 'Тараз', 'category': 'Животные',
        'title': 'Мейн-кун, 4 месяца, шоу-класс',
        'description': 'Продается котенок мейн-кун шоу-класса. Мальчик, окрас MCO ns 22 (черный серебристый тигровый). Оба родителя — чемпионы WCF. Ветпаспорт, все прививки, чип, клеймо. Документы WCF. Приучен к лотку и когтеточке.',
        'price': 350000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1518791841217-8f162f1912da?w=700&q=80',
    },
    {
        'city': 'Павлодар', 'category': 'Электроника',
        'title': 'Студийный монитор Genelec 8351B, пара',
        'description': 'Продаю пару студийных мониторов Genelec 8351B SAM. Три усилителя, встроенная DSP-коррекция. Диапазон 32 Гц — 40 кГц. Идеальное состояние, использовались в домашней студии. Комплект: мониторы, кабели, руководство по калибровке.',
        'price': 2100000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=700&q=80',
    },
    {
        'city': 'Павлодар', 'category': 'Работа',
        'title': 'UX/UI дизайнер в продуктовую команду',
        'description': 'Ищем UX/UI дизайнера в продуктовую команду EdTech компании. Требования: Figma на продвинутом уровне, опыт в мобильном дизайне от 2 лет, портфолио с кейсами. Задачи: проектирование новых фич, дизайн-система, работа с исследованиями. ЗП: 350 000 тг.',
        'price': 0, 'is_top': False,
        'image_url': '',
    },
    {
        'city': 'Өскемен', 'category': 'Авто',
        'title': 'Land Rover Defender 110 V8, 2022',
        'description': 'Land Rover Defender 110 V8 Carpathian Edition 2022. Объем 5.0L, 525 л.с. Пробег 18 000 км. Эксклюзивный цвет Carpathian Grey. Пакет Explorer: экспедиционный рейлинг, дополнительные фары, защита днища. Сервисная книжка официального дилера.',
        'price': 82000000, 'is_top': True,
        'image_url': 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=700&q=80',
    },
    {
        'city': 'Өскемен', 'category': 'Недвижимость',
        'title': 'Коммерческое помещение 240 кв.м, центр',
        'description': 'Продается коммерческое помещение в центре города. Площадь 240 кв.м, первый этаж, отдельный вход с улицы. Высокий трафик, рядом банки и торговые центры. Подходит под ресторан, шоу-рум, офис. Документы готовы.',
        'price': 145000000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=700&q=80',
    },
    {
        'city': 'Семей', 'category': 'Спорт',
        'title': 'Горные лыжи Völkl Blaze 106, 177 см',
        'description': 'Продаю горные лыжи Völkl Blaze 106, длина 177 см. Крепления Marker Griffon 13 ID. Использовались два сезона, состояние хорошее. Подходят для фрирайда и глубокого снега. В комплекте лыжный мешок Völkl.',
        'price': 290000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1551524559-8af4e6624178?w=700&q=80',
    },
    {
        'city': 'Семей', 'category': 'Услуги',
        'title': 'Фотограф и видеограф — свадьбы и события',
        'description': 'Профессиональный фотограф и видеограф с 8-летним опытом. Съемка свадеб, корпоративов, рекламы. Оборудование: Sony A7IV, дроны DJI, профессиональный свет. Монтаж в цвете. Смотрите портфолио на сайте. Бронируйте дату заранее.',
        'price': 150000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=700&q=80',
    },
    {
        'city': 'Атырау', 'category': 'Электроника',
        'title': 'Телевизор Samsung Neo QLED 8K 85"',
        'description': 'Samsung Neo QLED 8K 85 дюймов (QN800C). Разрешение 7680x4320, частота 120 Гц, Mini LED подсветка. Звук 60 Вт. Smart TV, Tizen OS. Куплен 6 месяцев назад, в идеальном состоянии. Настенное крепление в подарок.',
        'price': 1650000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f4834c?w=700&q=80',
    },
    {
        'city': 'Атырау', 'category': 'Разное',
        'title': 'Вино Pétrus 2015, коллекционное',
        'description': 'Продаю 3 бутылки Château Pétrus 2015 года. Хранение в профессиональном винном холодильнике при постоянной температуре 12°C. Оригинальные деревянные кейсы с сертификатами. Покупка подтверждена накладными из Bordeaux.',
        'price': 4500000, 'is_top': False,
        'image_url': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=700&q=80',
    },
]


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными для AnsarKin'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='ansarkin').exists():
            User.objects.create_superuser('ansarkin', 'ansarkin@gmail.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Суперпользователь: ansarkin / admin123'))

        seller, _ = User.objects.get_or_create(
            username='ansarkin_user',
            defaults={
                'first_name': 'Ансар',
                'last_name': 'Кинжегулов',
                'email': 'ansarkin@gmail.com',
            }
        )
        seller.set_password('admin123')
        seller.save()
        self.stdout.write(self.style.SUCCESS('Пользователь: ansarkin_user / admin123'))

        for name in CITIES:
            City.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Городов: {City.objects.count()}'))

        for name in CATEGORIES:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Категорий: {Category.objects.count()}'))

        count = 0
        for data in ADS_DATA:
            city = City.objects.get(name=data['city'])
            category = Category.objects.get(name=data['category'])
            if not Ad.objects.filter(title=data['title']).exists():
                Ad.objects.create(
                    author=seller,
                    city=city,
                    category=category,
                    title=data['title'],
                    description=data['description'],
                    price=data['price'],
                    is_top=data['is_top'],
                    is_moderated=True,
                    image_url=data.get('image_url', ''),
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Создано объявлений: {count}'))
        self.stdout.write(self.style.SUCCESS('База данных AnsarKin заполнена!'))
