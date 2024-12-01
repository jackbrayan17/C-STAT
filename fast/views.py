from rest_framework import viewsets, permissions
from fast.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreateForm
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .you import consolidate_data  # Import your consolidation function
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .variation import calculate_variation

@csrf_exempt
def process_folder(request):
    if request.method == 'POST':
        uploaded_folder = request.FILES.getlist('folder')
        if not uploaded_folder:
            return JsonResponse({'error': 'No folder uploaded!'}, status=400)

        # Create a temporary directory to save uploaded files
        temp_folder = 'uploaded_temp_folder'
        os.makedirs(temp_folder, exist_ok=True)

        # Save files to temp folder
        for f in uploaded_folder:
            file_path = os.path.join(temp_folder, f.name)
            with open(file_path, 'wb') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        # Call your consolidation logic
        output_folder = 'output'
        os.makedirs(output_folder, exist_ok=True)
        output_file = consolidate_data(
            files=[os.path.join(temp_folder, f.name) for f in uploaded_folder],
            output_folder=output_folder,
            base_filename="ConsolidatedTrimester"
        )

        # Debugging: Check if the file exists in the output folder
        output_file_path = os.path.join(output_folder, output_file)
        if not os.path.exists(output_file_path):
            return JsonResponse({'error': 'Consolidated file was not generated'}, status=500)

        # Clean up temporary folder
        for file_name in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, file_name))
        os.rmdir(temp_folder)

        # Pass the correct filename to the template
        return render(request, 'upload_folder.html', {'generated_file_name': output_file})

    return render(request, 'upload_folder.html')

from .variation import calculate_variation
import os
from django.http import HttpResponse, Http404
def ensure_var_directory():
    var_directory = os.path.join(os.path.dirname(__file__), 'var')
    if not os.path.exists(var_directory):
        os.makedirs(var_directory)  # Create the 'var' directory if it doesn't exist
    return var_directory
def calc_variation(request):
    generated_file_name = None
    
    if request.method == 'POST' and request.FILES['trim1'] and request.FILES['trim2']:
        trim1 = request.FILES['trim1']
        trim2 = request.FILES['trim2']
        
        # # Save uploaded files
        # fs = FileSystemStorage()
        # file1 = fs.save(trim1.name, trim1)
        # file2 = fs.save(trim2.name, trim2)
        
        # # Get the full file paths
        # file1_path = fs.url(file1)
        # file2_path = fs.url(file2)
        
        # Calculate variation
        output_file = calculate_variation(trim1, trim2)
        
        # Store the generated file name for rendering
        generated_file_name = os.path.basename(output_file)
        
        return render(request, 'calc_variation.html', {'generated_file_name': generated_file_name})
    
    return render(request, 'calc_variation.html')

def download_variation_file(request, file_name):
    # Ensure 'var' directory exists
    var_directory = os.path.join(os.path.dirname(__file__), 'var')
    file_path = os.path.join(var_directory, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    else:
        raise Http404("File not found")
def calc_variation_rates(request):
    # Logic for the "Calc Variation Rates" page
    return render(request, 'calc_variation_rates.html')

from django.http import FileResponse, JsonResponse
import os
def download_file(request, filename):
    file_path = os.path.join('output', filename)  # Ensure the path is correct
    if not os.path.exists(file_path):
        return JsonResponse({'error': f"File '{filename}' wasn't found."}, status=404)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
# Admin dashboard view
def admin_dashboard(request):
    users = User.objects.all()
    
    if request.method == 'POST':
        if 'create' in request.POST:
            form = UserCreateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "User created successfully.")
                return redirect('admin_dashboard')
        elif 'block' in request.POST:
            user_id = request.POST.get('block_user')
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            messages.success(request, "User blocked successfully.")
        elif 'unblock' in request.POST:
            user_id = request.POST.get('unblock_user')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            messages.success(request, "User unblocked successfully.")
        elif 'delete' in request.POST:
            user_id = request.POST.get('delete_user')
            user = User.objects.get(id=user_id)
            user.delete()
            messages.success(request, "User deleted successfully.")
    
    return render(request, 'admin_dashboard.html', {'users': users})


def home_page(request):
    context = {
        'username': request.user.username if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)
def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     @action(detail=True, methods=['post'])
#     def block(self, request, pk=None):
#         user = self.get_object()
#         user.is_blocked = True
#         user.save()
#         return Response({'status': 'user blocked'})

#     @action(detail=True, methods=['post'])
#     def unblock(self, request, pk=None):
#         user = self.get_object()
#         user.is_blocked = False
#         user.save()
#         return Response({'status': 'user unblocked'})

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    def get(self, request):
        return Response({"message": "Use POST to submit signup data."}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to the login page after successful signup
            return redirect('login')  # Use the name of your login URL pattern here
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.models import User

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # token, created = Token.objects.get_or_create(user=user)
            # Redirect to the home page after successful login
            # print("Token Created:", token.key)
            next_url = request.GET.get('next', 'home_page')
            return redirect(next_url)  # Use the name of your home URL pattern here
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# from rest_framework import generics, serializers
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group

# # Serializer to handle user data
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'is_active']

# # Serializer to handle user creation with role
# class UserCreateSerializer(serializers.ModelSerializer):
#     role = serializers.ChoiceField(choices=['supervisor', 'analyst', 'viewer'])

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'role']

#     def create(self, validated_data):
#         role = validated_data.pop('role')
#         user = User.objects.create_user(**validated_data)
        
#         # Assign role to the user
#         group, created = Group.objects.get_or_create(name=role)
#         user.groups.add(group)
#         user.save()
#         return user

# # List and create users for admin
# class UserListCreateAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Ensure only admin can create users
#         if self.request.user.is_superuser:
#             serializer.save()
#         else:
#             raise PermissionError("You do not have permission to create a user.")

# # View details, update or delete a user
# class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_update(self, serializer):
#         if self.request.user.is_superuser:
#             serializer.save()
#         else:
#             raise PermissionError("You do not have permission to update this user.")

#     def perform_destroy(self, instance):
#         if self.request.user.is_superuser:
#             instance.delete()
#         else:
#             raise PermissionError("You do not have permission to delete this user.")
