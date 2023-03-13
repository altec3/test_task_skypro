from django.db import models


class BaseClass(models.Model):
    """Базовый класс"""

    title = models.CharField(verbose_name='Название', max_length=255)

    class Meta:
        abstract = True


class Contacts(models.Model):
    """Контакты"""

    email = models.EmailField(verbose_name='Email',)
    country = models.CharField(verbose_name='Страна', blank=True, null=True, max_length=50,)
    city = models.CharField(verbose_name='Город', blank=True, null=True, max_length=50,)
    street = models.CharField(verbose_name='Улица', blank=True, null=True, max_length=255,)
    house = models.PositiveSmallIntegerField(verbose_name='Номер дома', blank=True, null=True,)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.email


class Product(BaseClass):
    """Продукт"""

    model = models.CharField(verbose_name='Модель', blank=True, null=True, max_length=255,)
    release = models.DateTimeField(verbose_name='Дата выхода на рынок', null=True,)

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
                                 on_delete=models.PROTECT,
                                 )
    type = models.PositiveSmallIntegerField(verbose_name='Тип',
                                            choices=Type.choices,
                                            default=Type.factory,
                                            )

    class Meta:
        verbose_name = 'Распространитель'
        verbose_name_plural = 'Распространители'

    def __str__(self):
        return self.title


class Link(models.Model):
    """Звено сети"""

    products = models.ManyToManyField(Product,
                                      verbose_name='Продукция',
                                      related_name='product_links',
                                      blank=True,
                                      )
    distributor = models.ForeignKey(Distributor,
                                    verbose_name='Распространитель продукции',
                                    related_name='link_distributor',
                                    on_delete=models.PROTECT,
                                    )
    supplier = models.ForeignKey(Distributor,
                                 verbose_name='Поставщик продукции',
                                 related_name='link_supplier',
                                 blank=True,
                                 null=True,
                                 on_delete=models.PROTECT,
                                 )
    debt = models.DecimalField(verbose_name='Задолженность перед поставщиком',
                               max_digits=19,
                               decimal_places=2,
                               default=0.00,
                               )
    country = models.CharField(verbose_name='Страна', blank=True, null=True, max_length=50,)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True,)

    class Meta:
        verbose_name = 'Звено сети продаж'
        verbose_name_plural = 'Звенья сети продаж'
        ordering = ['pk']

    def __str__(self):
        return self.distributor.title


class Network(BaseClass):
    """Сеть продаж"""

    manufacturer = models.ForeignKey(Link,
                                     verbose_name='Производитель продукции',
                                     on_delete=models.PROTECT,
                                     )
    distributor_1 = models.ForeignKey(Link,
                                      verbose_name='Распространитель №1',
                                      related_name='net_distributor_1',
                                      blank=True,
                                      null=True,
                                      on_delete=models.PROTECT,
                                      )
    distributor_2 = models.ForeignKey(Link,
                                      verbose_name='Распространитель №2',
                                      related_name='net_distributor_2',
                                      blank=True,
                                      null=True,
                                      on_delete=models.PROTECT,
                                      )

    class Meta:
        verbose_name = 'Сеть продаж'
        verbose_name_plural = 'Сети продаж'

    def __str__(self):
        return self.title
