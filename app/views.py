from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.db.models import Count
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import check_password
import base64
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
import datetime
import re
from urllib.parse import quote
from django.utils.timezone import now
import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.

def get_client_ip(request):
    """
    Retrieves the client's IP address from the HTTP request.

    If the client is behind a proxy, the function will attempt to get the original
    IP address from the 'HTTP_X_FORWARDED_FOR' header, which typically contains
    a list of IP addresses. It takes the first one, assuming it to be the original
    client IP.

    If the 'HTTP_X_FORWARDED_FOR' header is not present, the function falls back 
    to getting the IP address directly from the 'REMOTE_ADDR' header, which 
    contains the address from which the request was made.

    :param request: The HTTP request object.
    :return: The client's IP address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        # If the request has passed through a proxy, the first IP in the list is the client IP
        ip = x_forwarded_for.split(',')[0]
    else:
        # If no proxy, get the direct IP address of the client
        ip = request.META.get('REMOTE_ADDR')
    
    return ip

def homepage(request):
    return render(request, "main/home.html")

def login(request):  # Renamed to avoid conflict with built-in login()
    if request.method == 'POST':
        username = request.POST.get('username').strip()  # Get email from the login form
        password = request.POST.get('password').strip()

        # Use email as the username field for authentication
        user = authenticate(username=username, password=password)  

        if user is not None:
            # Use Django's built-in login function (aliased as auth_login)
            auth_login(request, user)
            return redirect('index')  # Redirect to the homepage
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, "authenticate/login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')

def signUp(request):
    if request.method == 'POST':
        username = request.POST['username'].strip() # Use registration number as username
        email = request.POST['email']
        password = request.POST['pssword1']
        confirm_password = request.POST['pssword2']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if password length is at least 8 characters
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('signup')

        # Check if password contains both letters and numbers
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            messages.error(request, 'Password must contain both letters and numbers.')
            return redirect('signup')

        # Check if email is valid
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Create user with a random username if everything is valid

        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
        )
        #user.is_active=False
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
        #messages.success(request, "Account created successfully. Check Email to activate.")
    return render(request, 'authenticate/signup.html')

@login_required(login_url='login')
def index(request):
    posts = Post.objects.annotate(comment_count=Count("comments")).order_by("-created_on")  # Fetch all posts
    # Ensure the logged-in user has a profile

    profile = Profile.objects.filter(user=request.user).first()
    
    if profile:
        return render(request, "main/main.html", {'posts': posts})
    else:
        messages.info(request, 'Please create a profile first.')
        return render(request, "main/main.html", {'posts': posts})

        #from urllib.parse import quote
        #encoded_username = quote(request.user.username, safe='')
        #return redirect('create_profile', username=encoded_username)
     
@login_required(login_url='login')
def manage_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio', profile.bio)
        date_of_birth = request.POST.get('date_of_birth', profile.date_of_birth)

        cover_img = request.FILES.get('cover_img')
        profile_img = request.FILES.get('profile_img')

        profile.bio = bio
        profile.date_of_birth = date_of_birth

        if cover_img:
            profile.cover_img = cover_img
        if profile_img:
            profile.profile_img = profile_img

        profile.save()

        messages.success(request, "Profile updated successfully! 👍" if not created else "Profile created successfully! 🎉")
        
        #encoded_username = quote(request.user.username, safe='')  # URL-encode
        #return redirect('profile', username=encoded_username)
        return redirect("index")

    return render(request, 'settings/create_profile.html', {'profile': profile})

@login_required(login_url='login')
def post_1(request):
    try:
        if request.method == 'POST':
            post_caption = request.POST.get('post-caption', '')

            request.session['post_caption'] = post_caption

            return redirect('post_2')
        #else:
            #messages.info(request, "Unable to process your request, Report issue to the Admin, Err:0001")
            #return render(request, "main/post1.html")
    except Exception as Err:
        messages.info(request, f"Error: {Err}")
    return render(request, "main/post1.html")

@login_required(login_url='login')
def post_2(request):
    if request.method == 'POST':
        post_image = request.FILES.get('post-image')
        post_url_1 = request.POST['post-url-1']
        post_url_2 = request.POST['post-url-2']
        post_url_3 = request.POST['post-url-3']

        new_post = Post.objects.create(
            user_id = request.user.id,
            post_caption = request.session.get('post_caption'),
            post_image = post_image,
            url1 = post_url_1,
            url2 = post_url_2,
            url3 = post_url_3,
        )
        new_post.save()

        ##### Clearing the session #####
        keys_to_clear = ['post_caption']

        for key in keys_to_clear:
            request.session.pop(key, None)
        ###########################################
        messages.info(request, "Post posted successful ")
        return redirect('index')
    #else:
        #messages.info(request, "Unable to Post, Error:0002 ")
    return render(request, "main/post2.html")

@login_required(login_url='login')
def comments(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    comments = Comment.objects.filter(comment_post=post).order_by("-comment_id")  # Latest comments first

    if request.method == "POST":
        caption = request.POST.get("caption", "").strip()
        comment_url = request.POST.get("comment_url", "")

        if caption:  # Ensure comment is not empty
            Comment.objects.create(
                users=request.user,
                comment_post=post,
                comment_caption=caption,
                comment_url=comment_url,
                comment_date=now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
            )

        return redirect("comment", post_id=post_id)  # Refresh page after comment submission

    return render(request, 'main/comment/comment.html', {"post": post, "comments": comments})

@login_required(login_url='login')
def delete(request, post_id):
    post = Post.objects.get(post_id=post_id)
    if request.user == post.user:
        try:
            post.delete()
            messages.success(request, "Post deleted successfully")
            return redirect('index')
        except Exception as error:
            messages.info(request, f"Unable to delete.")

@login_required(login_url='login')
def profile(request):
    # Ensure the logged-in user has a profile
    
    #from urllib.parse import quote
    #encoded_username = quote(request.user.username, safe='') 
    try:
        profile = Profile.objects.get(user=request.user)

    except Profile.DoesNotExist:
        return redirect('create_profile')

    # Fetch the profile and posts of the requested user
    user = get_object_or_404(User, username=request.user.username)
    user_posts = Post.objects.filter(user=user).annotate(comment_count=Count("comments")).order_by("-created_on")
    user_profile = get_object_or_404(Profile, user=user)

    return render(request, 'main/profile.html', {
        'user': user,
        'user_profile': user_profile,
        'user_posts': user_posts
    })

@login_required(login_url='login')
def search(request):
    query = request.GET.get("q", "").strip()
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    context = {"query": query, "users": users}
    return render(request, 'main/search.html', context)


@login_required(login_url='login')
def settings(request):
    return render(request, 'settings/settings.html')

@login_required(login_url='login')
def profile_settings(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'settings/profile_settings/profile_settings.html', {'profile': profile})

@login_required(login_url='login')
def edit_account(request):
    if request.method == 'POST':
        user = request.user
        #username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Ensure username and email are unique
        #if User.objects.exclude(pk=user.pk).filter(username=username).exists():
        #    messages.error(request, "Username already taken!")
        #    return redirect('edit_account')

        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect('edit_account')

        # Update user info
        #user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Handle password update
        if password:
            if password == confirm_password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # Keep user logged in after password change
                messages.success(request, "Account updated successfully! 🎉")
            else:
                messages.error(request, "Passwords do not match!")
                return redirect('edit_account')

        user.save()
        messages.success(request, "Account updated successfully! 🎉")
        return redirect('profile')

    return render(request, 'settings/edit_account.html')


def about(request):
    return render(request, "settings/about.html")

def terms(request):
    return render(request, "settings/terms.html")

def privacy(request):
    return render(request, "settings/privacy.html")

@login_required(login_url='login')
def feedback(request):
    return render(request, "settings/feedback.html")
