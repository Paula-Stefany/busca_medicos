from django.forms import ModelForm 
from medicSearch.models.Address import Address
from medicSearch.models.Neighborhood import Neighborhood
from medicSearch.models.City import City
from medicSearch.models.State import State
from medicSearch.models.Profile import Profile
from medicSearch.models.DayWeek import DayWeek
from django import forms


class AddressForm(ModelForm):

    class Meta:
        model = Address
        fields = ['address', 'consultory_name', 'opening_time', 'closing_time', 'phone', 'latitude', 'longitude', 'days_week']

        labels = {
            'consultory_name': '* Nome do consultório',
            'address': '* Endereço',
            'opening_time': '* Horário de abertura',
            'closing_time': '* Horário de fechamento',
            'latitude': '* Latitude',
            'longitude': '* Longitude',
            'days_week': '* Dias da semana'
        }

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'consultory_name': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control'}),    
            'days_week': forms.widgets.SelectMultiple(attrs={'class': 'form-control'})
        }


class NeighborhoodForm(ModelForm):

    class Meta:
        model = Neighborhood
        fields = ['neighborhood_name']

        labels = {
            'neighborhood_name': '* Bairro',
        }
        
        widgets = {
            'neighborhood_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CityForm(ModelForm):

    class Meta:
        model = City 
        fields = ['city_name']

        labels = {
            'city_name': '* Cidade'
        }

        widgets = {
            'city_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class StateForm(ModelForm):

    class Meta:
        model = State
        fields = ['state_name']

        labels = {
            'state_name': '* Estado'
        }

        widgets = {
            'state_name': forms.TextInput(attrs={'class': 'form-control'})
        }
