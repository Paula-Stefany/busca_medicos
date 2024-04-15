from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'   
    list_display = ('user', 'role', 'specialtiesList', 'addressesList', 'birth')
    empty_value_display = 'vazio'
    list_display_links = ('user', 'role', 'specialtiesList', 'addressesList', 'birth')
    list_filter = ('user__is_active',)
    fieldsets = (
        ('Perfil do Usuário', {'fields': ('user', 'role', 'birthday', 'image')}),
        ('Área de Atuação', {'fields': ('specialties',)}),
        ('Localização', {'fields': ('addresses',)}),
    )
    exclude = ('favorites', 'created_at', 'updated_at',)
    readonly_fields = ('user',)
    search_fields = ('user__username',)

    def birth(self, obj):
        if obj.birthday:
            return obj.birthday.strftime('%d/%m/%Y')
    birth.empty_value_display = '__/__/____'

    def specialtiesList(self, obj):
        specialties_name = [i.name for i in obj.specialties.all()]
        return specialties_name if specialties_name else '---'
    
    def addressesList(self, obj):
        addresses_name = [f'{address.consultory_name} - {address.address} - {address.neighborhood} - {address.neighborhood.city.state}'for address in obj.addresses.all()]
        return addresses_name if addresses_name else '---'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(Address)
admin.site.register(DayWeek)
admin.site.register(Rating)
admin.site.register(Speciality)
