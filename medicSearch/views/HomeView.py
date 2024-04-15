from django.shortcuts import render
from medicSearch.models.City import City
from medicSearch.models.State import State
from medicSearch.models.Neighborhood import Neighborhood
from medicSearch.models.Speciality import Speciality


def home_view(request):
    all_cities = City.objects.all()
    all_states = State.objects.all()
    all_neighborhoods = Neighborhood.objects.all()
    specialties = Speciality.objects.all()

    unique_states = {}
    for state in all_states:
        unique_states[state.state_name.lower()] = state 
    
    unique_cities = {}
    for city in all_cities:
        unique_cities[city.city_name.lower()] = city 

    unique_neighborhoods = {}
    for neighborhood in all_neighborhoods:
        unique_neighborhoods[neighborhood.neighborhood_name.lower()] = neighborhood

    states = list(unique_states.values())
    cities = list(unique_cities.values())
    neighborhoods = list(unique_neighborhoods.values())

    context = {
        'cities': cities,
        'states': states,
        'neighborhoods': neighborhoods,
        'specialties': specialties
    }
    return render(request, template_name='home/home.html', context=context, status=200)
