from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from medicSearch.models import Profile
from django.core.paginator import Paginator
from medicSearch.forms.UserProfileForm import UserProfileForm, UserForm


def list_profile_view(request, id=None):
    profile= None    
    ratings = []
    favorites = []

    if id is None and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    elif id is not None:
        profile = Profile.objects.filter(id=id).first()

    elif not request.user.is_authenticated:
        return redirect(to='/')
    
    if profile.role != 2:
        favorites = profile.show_favorites()
   
    if len(favorites) > 0:
        paginator = Paginator(favorites, 8)
        page = request.GET.get('page')
        favorites = paginator.get_page(page)

    if profile is not None and profile.role == 2: 
        ratings = profile.show_ratings()
    
        if len(ratings) > 0:
            paginator = Paginator(ratings, 8)
            page = request.GET.get('page')
            ratings = paginator.get_page(page)

    context = {
        'profile': profile,
        'favorites': favorites,
        'ratings': ratings
    }

    return render(request, template_name='profile/profile.html', context=context, status=200)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    emailUnused = True
    message = None

    if request.method == 'POST':
        profileForm = UserProfileForm(request.POST, request.FILES, instance=profile)
        userForm = UserForm(request.POST,  instance=request.user)

        verifyEmail = Profile.objects.filter(user__email = request.POST['email']).exclude(user__id=request.user.id).first()
        emailUnused = verifyEmail is None
    else:
        profileForm = UserProfileForm(instance=profile)
        userForm = UserForm(instance=request.user)
    
    if profileForm.is_valid() and userForm.is_valid() and emailUnused:
        profileForm.save()
        userForm.save()
        message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
    
    else:
        if request.method == 'POST':
            if emailUnused:
                message = {'type': 'danger', 'text': 'Dados inválidos'}
            else:
                message = {'type': 'warning', 'text': 'E-mail já usado por outro usuário'}

    context = {
        'profileForm': profileForm,
        'userForm': userForm,
        'message': message
    }

    return render(request, template_name='user/profile.html', context=context, status=200)