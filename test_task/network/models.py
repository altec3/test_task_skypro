from django.db import models


class BaseClass(models.Model):
    """Базовый класс"""

    title = models.CharField(verbose_name='Название', max_length=255)

    class Meta:
        abstract = True


class Contacts(models.Model):
    """Контакты"""

    email = models.EmailField(verbose_name='Email')
    country = models.CharField(verbose_name='Страна', blank=True, null=True, max_length=50)
    city = models.CharField(verbose_name='Город', blank=True, null=True, max_length=50)
    street = models.CharField(verbose_name='Улица', blank=True, null=True, max_length=255)
    house = models.PositiveSmallIntegerField(verbose_name='Номер дома', null=True)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.email


class Product(BaseClass):
    """Продукт"""

    model = models.CharField(verbose_name='Модель', blank=True, null=True, max_length=255)
    release = models.DateTimeField(verbose_name='Дата выхода на рынок', null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Distributor(BaseClass):
    """Распространитель продукции"""

    class Type(models.IntegerChoices):
        factory = 1, 'Завод'
        retail = 2, 'Розничная сеть'
        self_employed = 3, 'Индивидуальный предприниматель'

    contacts = models.ForeignKey(Contacts,
                                 verbose_name='Контакты',
                                 related_name='distributors',
                                 on_delete=models.PROTECT
                                 )
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                related_name='distributors',
                                on_delete=models.PROTECT
                                )
    type = models.PositiveSmallIntegerField(verbose_name='Тип', choices=Type.choices, default=Type.factory)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Распространитель'
        verbose_name_plural = 'Распространители'

    def __str__(self):
        return self.title


class Network(models.Model):
    """Сеть продаж"""

    distributor = models.ForeignKey(Distributor,
                                    verbose_name='Распространитель продукции',
                                    related_name='net_distributors',
                                    on_delete=models.PROTECT
                                    )
    supplier = models.ForeignKey(Distributor,
                                 verbose_name='Поставщик',
                                 related_name='net_suppliers',
                                 null=True,
                                 on_delete=models.PROTECT
                                 )
    debt = models.BigIntegerField(verbose_name='Задолженность', default=0)

    class Meta:
        verbose_name = 'Сеть продаж'
        verbose_name_plural = 'Сети продаж'

    def __str__(self):
        return self.title
