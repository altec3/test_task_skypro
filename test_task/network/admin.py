from django.contrib import admin, messages
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import ngettext

from network.models import Contacts, Product, Distributor, Network, Link


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    """Регистрация модели Contacts для отображения в панели администратора"""

    list_display = ('email', 'country', 'city', 'street', 'house',)
    search_fields = ('email', 'country',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели Product для отображения в панели администратора"""

    list_display = ('title', 'model', 'release',)
    search_fields = ('title', 'model',)


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    """Регистрация модели Distributor для отображения в панели администратора"""

    list_display = ('title', 'contacts', 'type',)
    search_fields = ('title', 'contacts__email', 'contacts__country',)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """Регистрация модели Link для отображения в панели администратора"""

    list_display = ('get_products', 'distributor', 'supplier_link', 'debt', 'country', 'created',)
    search_fields = ('distributor__title', 'supplier__title',)
    readonly_fields = ('created',)
    list_filter = ('country',)

    #: Реализация admin action
    actions = ['clear_debt']

    @admin.action(description='Очистить задолженность')
    def clear_debt(self, request: WSGIRequest, queryset: QuerySet):
        updated = queryset.update(debt=0)
        self.message_user(request, ngettext(
            'Успешно удалена %d задолженность',
            'Успешно удалено %d задолженности',
            updated,
        ) % updated, messages.SUCCESS)

    #: Реализация отображения ManyToManyField
    def get_products(self, obj: Link):
        return ", ".join([p.model for p in obj.products.all()])
    get_products.short_description = 'Продукция'

    #: Реализация ссылки на Поставщика
    def supplier_link(self, obj: Link):
        if obj.supplier:
            from django.utils.html import format_html
            url = u'<a href="{0}">{1}</a>'.format(
                reverse('admin:network_distributor_change', args=(obj.supplier.id,)),
                obj.supplier
            )
            return format_html(url)
    supplier_link.short_description = 'Поставщик продукции'


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    """Регистрация модели Network для отображения в панели администратора"""

    list_display = ('title', 'manufacturer_link', 'distributor_1_link', 'distributor_2_link',)
    search_fields = (
        'manufacturer__distributor__title',
        'distributor_1__distributor__title',
        'distributor_2__distributor__title',
    )

    #: Реализация ссылки на Производителя продукции
    def manufacturer_link(self, obj: Network):
        if obj.manufacturer:
            from django.utils.html import format_html
            url = u'<a href="{0}">{1}</a>'.format(
                reverse('admin:network_link_change', args=(obj.manufacturer.pk,)),
                obj.manufacturer
            )
            return format_html(url)
    manufacturer_link.short_description = 'Производитель продукции'

    #: Реализация ссылки на Поставщика №1
    def distributor_1_link(self, obj: Network):
        if obj.distributor_1:
            from django.utils.html import format_html
            url = u'<a href="{0}">{1}</a>'.format(
                reverse('admin:network_link_change', args=(obj.distributor_1.pk,)),
                obj.distributor_1
            )
            return format_html(url)
    distributor_1_link.short_description = 'Поставщик №1'

    #: Реализация ссылки на Поставщика №2
    def distributor_2_link(self, obj: Network):
        if obj.distributor_2:
            from django.utils.html import format_html
            url = u'<a href="{0}">{1}</a>'.format(
                reverse('admin:network_link_change', args=(obj.distributor_2.pk,)),
                obj.distributor_2
            )
            return format_html(url)
    distributor_2_link.short_description = 'Поставщик №2'
