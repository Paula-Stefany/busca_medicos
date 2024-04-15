from django.contrib.auth.decorators import login_required
from medicSearch.models import Profile, Rating
from medicSearch.forms.MedicForm import MedicRatingForm
from django.db.models import Q 
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator  
from medicSearch.forms.AddressForm import AddressForm, NeighborhoodForm, CityForm, StateForm
from medicSearch.models.Address import Address
from medicSearch.models.Neighborhood import Neighborhood
from medicSearch.models.City import City
from medicSearch.models.State import State
from medicSearch.models.DayWeek import DayWeek
from django.db import transaction
from django.db.models import Count
from collections import Counter


def list_medics_view(request):
    name = request.GET.get('name')
    speciality = request.GET.get('speciality')
    neighborhood = request.GET.get('neighborhood')
    city = request.GET.get('city')
    state = request.GET.get('state')
    
    medics = Profile.objects.filter(role=2)

    if name is not None and name != '':
        medics = medics.filter(Q(user__first_name__contains = name) | Q(user__username__contains = name))
    if speciality is not None:
        medics = medics.filter(specialties__id = speciality)

    if neighborhood is not None:
        medics = medics.filter(addresses__neighborhood__neighborhood_name = neighborhood)
    else:
        if city is not None:
            medics = medics.filter(addresses__neighborhood__city__city_name = city)
        elif state is not None:
            medics = medics.filter(addresses__neighborhood__city__state__state_name = state)

    medics_list = list(medics)

    unique_medics = [] 
    seen = set()
    for medic in medics_list:
        if medic.user.username not in seen:
            unique_medics.append(medic)
            seen.add(medic.user.username)

    if len(medics) > 0:
        paginator = Paginator(unique_medics, 8)
        page = request.GET.get('page')
        medics = paginator.get_page(page)

    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()


    context = {
        'medics': unique_medics,
        'parameters': parameters
    }

    return render(request, template_name='medic/medics.html', context = context, status = 200)


def add_favorite_view(request):
    page = request.POST.get('page')
    name = request.POST.get('name')
    speciality = request.POST.get('speciality')
    neighborhood = request.POST.get('neighborhood')
    city = request.POST.get('city')
    state = request.POST.get('state')
    id = request.POST.get('id')

    try:
        profile = Profile.objects.filter(user=request.user).first()
        medic = Profile.objects.filter(user__id=id).first()
        profile.favorites.add(medic.user)
        profile.save()
        msg = 'Favorito adicionado com sucesso'
        _type= 'success'
    except Exception as e:
        print('Erro %s' % e)
        msg = 'Um erro ocorreu ao salvar o médico nos favoritos'
        _type = 'danger'
 
    if page:
        arguments = '?page=%s' % (page)
    else:
        arguments = '?page=1'
    if name:
        arguments += '&name=%s' % name
    if speciality:
        arguments += '&speciality=%s' % speciality
    if neighborhood:
        arguments += '&neighborhood=%s' % neighborhood
    if city:
        arguments += '&city=%s' % city
    if state:
        arguments += '&state=%s' % state

    arguments += '&msg=%s&type=%s' % (msg, _type)

    return redirect(to='/medic/%s' % arguments)

def remove_favorite_view(request):
    page = request.POST.get("page")
    id = request.POST.get("id")

    try:
        profile = Profile.objects.filter(user=request.user).first()
        medic = Profile.objects.filter(id=id).first()
        profile.favorites.remove(medic.user)
        profile.save()
        msg = "Favorito removido com sucesso."
        _type = "success"
    except Exception as e:
        print("Erro %s" % e)
        msg = "Um erro ocorreu ao remover o médico nos favoritos."
        _type = "danger"

    if page:
        arguments = "?page=%s" % (page)
    else:
        arguments = "?page=1"
    
    arguments += "&msg=%s&type=%s" % (msg, _type)
    return redirect(to='/profile/%s' % arguments)

@login_required
def rate_medic(request, medic_id=None):
   
    medic = Profile.objects.filter(user__id=medic_id).first()
    
    rating = Rating.objects.filter(user=request.user, user_rated=medic.user).first()
    message = None 
    initial = {'user': request.user, 'user_rated': medic.user}

    if request.method == 'POST':
        ratingForm = MedicRatingForm(request.POST, instance=rating, initial=initial)
    else:
        ratingForm = MedicRatingForm(instance=rating, initial=initial)
    if ratingForm.is_valid():
        ratingForm.save()
        message = {'type': 'success', 'text': 'Avaliação salva com sucesso'}
    else:
        if request.method == 'POST':
            message = {'type': 'danger', 'text': 'Erro ao salvar avaliação'}

    context = {
        'ratingForm': ratingForm,
        'medic': medic,
        'message': message
    }

    return render(request, template_name='medic/rating.html', context=context, status=200)


def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id) 
    message = None
  
    if request.method == 'POST':
        neighborhood_form = NeighborhoodForm(request.POST, request.FILES, instance=address.neighborhood)
        city_form = CityForm(request.POST, request.FILES, instance=address.neighborhood.city)
        state_form = StateForm(request.POST, request.FILES, instance= address.neighborhood.city.state)
        address_form = AddressForm(request.POST, request.FILES, instance= address)

        if neighborhood_form.is_valid() and city_form.is_valid() and state_form.is_valid() and address_form.is_valid():
            

            same_address = _check_duplicate_address(address_form, neighborhood_form, city_form, state_form)

            other_profiles = Profile.objects.filter(addresses=address).exclude(id=request.user.profile.id)


            if same_address and other_profiles.exists():  
                request.user.profile.addresses.remove(address)
                request.user.profile.addresses.add(same_address)
                message= {'type': 'success', 'text': 'Dados atualizados com sucesso'}

            elif same_address and not other_profiles.exists():
                request.user.profile.addresses.remove(address)
                request.user.profile.addresses.add(same_address)
                address.delete()
                message= {'type': 'success', 'text': 'Dados atualizados com sucesso'}

            else:
                other_profiles = Profile.objects.filter(addresses=address).exclude(id=request.user.profile.id)

                if not other_profiles.exists():

                    _update_address(state_form, city_form, neighborhood_form, address_form)

                    message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
                
                elif other_profiles.exists():
                    
                    new_address =_create_new_address(state_form, city_form, neighborhood_form, address_form)

                    request.user.profile.addresses.remove(address)
                    request.user.profile.addresses.add(new_address)

                    message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}

                else:
                    message = {'type': 'danger', 'text': 'Ocorreu um erro ao tentar editar seus dados :('}
        else:
            message = {'type': 'danger', 'text': 'Formulário inválido'}

    context = {
        'stateForm': StateForm(instance= address.neighborhood.city.state),
        'cityForm': CityForm(instance= address.neighborhood.city),
        'neighborhoodForm': NeighborhoodForm(instance= address.neighborhood),
        'addressForm': AddressForm(instance=address),
        'message': message
        }

    return render(request, template_name='user/address.html', context=context, status=200)


def _check_duplicate_address(address_form, neighborhood_form, city_form, state_form):

    same_address = Address.objects.filter(
        Q(consultory_name= address_form.cleaned_data['consultory_name']) &
        Q(address= address_form.cleaned_data['address']) &
        Q(opening_time= address_form.cleaned_data['opening_time']) &
        Q(closing_time= address_form.cleaned_data['closing_time']) &
        Q(phone= address_form.cleaned_data['phone']) &
        Q(latitude= address_form.cleaned_data['latitude']) &
        Q(longitude= address_form.cleaned_data['longitude']) &
        Q(days_week__in= address_form.cleaned_data['days_week']) &
        Q(neighborhood__neighborhood_name= neighborhood_form.cleaned_data['neighborhood_name']) &
        Q(neighborhood__city__city_name= city_form.cleaned_data['city_name']) &
        Q(neighborhood__city__state__state_name= state_form.cleaned_data['state_name'])
    ).first()

    return same_address 
    

def _update_address(state_form, city_form, neighborhood_form, address_form):

    state = state_form.save()
    city = city_form.save(commit=False)
    neighborhood = neighborhood_form.save(commit=False)
    address = address_form.save(commit=False)

    address.days_week.set(address_form.cleaned_data['days_week'])

    city.state = state 
    city.save()
    neighborhood.city = city 
    neighborhood.save()
    address.neighborhood = neighborhood 
    address.save()


def _create_new_address(state_form, city_form, neighborhood_form, address_form):

    new_state = State.objects.create(state_name = state_form.cleaned_data['state_name'])
    new_city = City.objects.create(state=new_state, city_name = city_form.cleaned_data['city_name'])
    new_neighborhood = Neighborhood.objects.create(city = new_city, neighborhood_name = neighborhood_form.cleaned_data['neighborhood_name'])

    new_address =  Address.objects.create(
        neighborhood= new_neighborhood,
        consultory_name= address_form.cleaned_data['consultory_name'],
        address= address_form.cleaned_data['address'],
        opening_time= address_form.cleaned_data['opening_time'],
        closing_time= address_form.cleaned_data['closing_time'], 
        phone= address_form.cleaned_data['phone'], 
        latitude= address_form.cleaned_data['latitude'], 
        longitude= address_form.cleaned_data['longitude'],
        days_week= address_form.cleaned_data['days_week']
        )

    new_address.days_week.add(*address_form.cleaned_data['days_week'])
    return new_address