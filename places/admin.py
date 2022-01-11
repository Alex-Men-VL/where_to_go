from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Place, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('img', 'place',)
    list_filter = ('place__title',)
    actions = ('change_the_order',)

    def save_model(self, request, obj, form, change):
        obj.number = Image.objects.filter(
            place=obj.place
        ).last().number + 1
        obj.save()

    @admin.action(description='Поменять местами')
    def change_the_order(self, request, queryset):
        if (queryset.count() != 2 or
                queryset[0].place != queryset[1].place):
            self.message_user(request,
                              'Выберите две картинки одного места, которые '
                              'хотите поменять местами.',
                              messages.ERROR)
        else:
            queryset[0].number, queryset[1].number = (queryset[1].number,
                                                      queryset[0].number)
            queryset[0].save()
            queryset[1].save()
            self.message_user(request,
                              'Картинки успешно поменяны местами.',
                              messages.SUCCESS)


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    fields = ('img', 'image_tag', 'number',)
    readonly_fields = ('image_tag',)
    extra = 1

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="auto" height="150" >',
            obj.img.url
        )

    image_tag.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ('title',)
