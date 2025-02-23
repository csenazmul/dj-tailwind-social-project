from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CustomLoginForm, ProfileUpdateForm
from .models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(author=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'user_posts': user_posts
    }
    return render(request, 'users/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def search_users(request):
    query = request.GET.get('query', '')
    if query:
        base_query = Q(username__icontains=query) | Q(email__icontains=query)
        
        # Create base queryset
        users = User.objects.filter(base_query).select_related('profile')
        
        # Exclude current user if logged in
        if request.user.is_authenticated:
            users = users.exclude(username=request.user.username)  # Using username for more reliable exclusion
            
        # Ensure the queryset is evaluated
        users = users.distinct()
    else:
        users = User.objects.none()  # Return empty queryset instead of empty list
    
    return render(request, 'users/search_results.html', {
        'users': users,
        'query': query
    })

def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=profile_user)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    return render(request, 'users/public_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts
    })


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page