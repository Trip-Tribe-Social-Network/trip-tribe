from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
        'bio': request.user.bio,  
        'friends': UserSerializer(request.user.friends.all(), many=True).data
    })

@api_view(['POST']) 
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return JsonResponse({'message': 'information updated', 'user': serializer.data})

@api_view(['POST'])
def edit_password(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'password updated'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        url = f'http://127.0.0.1:8000/activateemail/?email={user.email}&id={user.id}'

        send_mail(
            "Please verify your email address",
            f"The url for activating your account is: {url}",
            "noreply@triptribe.com",
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message}, safe=False)

@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    request_list = []

    u = request.user
    u.friends_count = 1
    u.save()

    user.friends_count = 1
    user.save()

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        request_list = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': request_list,
    })

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    existing_request = FriendshipRequest.objects.filter(
        created_for=user, created_by=request.user
    ).exclude(status=FriendshipRequest.REJECTED).exists()

    if not existing_request:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({'message': 'Friendship request created'})
    else:
        return JsonResponse({'message': 'Request already sent'})


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count += 1
    user.save()

    request_user = request.user
    request_user.friends_count += 1
    request_user.save()

    return JsonResponse({'message': 'friendship request updated'})