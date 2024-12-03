import base64
from django.shortcuts import render,redirect,HttpResponseRedirect # type: ignore
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm # type: ignore
from django.contrib.auth import authenticate # type: ignore
from django.core.files.storage import FileSystemStorage # type: ignore
from django.shortcuts import render, redirect
from demopage.forms import CustomUserCreationForm  # Import the custom form
from joblib import load

import cv2
import numpy as np
 
 
model = load('skin_disease_model.joblib')
 
# Create your views here.
def home(request):
    return render(request,'home.html')
 
def login(request):
    if(request.user.is_authenticated):
        return render(request,'login.html')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        #authenticate() is used to check for the values present in the database or not
        #if the values are matched, then it will return the username
        #if the values are not matched, then it will return as 'None'
        # use authenticate(), need to import it from auth package
        user = authenticate(request,username=un,password=pw)
        if(user is not None):
            return redirect('/profile/')
        else:
            msg = 'Invalid Username/Password'
            form = AuthenticationForm(request.POST)
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        #used to create a basic login page with username and password
        return render(request,'login.html',{'form':form})
# def login(request):
#     if(request.user.is_authenticated):
#         return redirect('/login')
#     if(request.method == "POST"):
#         un = request.POST['username']
#         pw = request.POST['password']
#         user = authenticate(request,username=un,password=pw)
#         if(user is not None):
#             return redirect('/profile')
#         else:
#             msg = 'Invalid Username/Password'
#             return render(request,'login.html',{'msg':msg})
#     else:
        # return render(request,'login.html')
        
#def signup
 
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')

#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             un = form.cleaned_data.get('username')
#             pw = form.cleaned_data.get('password1')

#             # Authenticate only if the password is not empty
#             if pw:
#                 user = authenticate(username=un, password=pw)
#                 if user is not None:
#                     return redirect('/login/')
#             return redirect('/login/')
#         else:
#             # Return errors to the template if form validation fails
#             return render(request, 'signup.html', {'form': form})

#     form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')

            # Authenticate only if the password is not empty
            if pw:
                user = authenticate(username=un, password=pw)
                if user is not None:
                    return redirect('/login/')
            return redirect('/login/')
        else:
            # Return errors to the template if form validation fails
            return render(request, 'signup.html', {'form': form})
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
# def register(request):
#     if(request.user.is_authenticated):
#         return redirect('/')
#     if(request.method == "POST"):
#         un = request.POST['username']
#         pw1 = request.POST['password']
#         pw2 = request.POST['confirmPassword']
#         user = authenticate(request,username=un)
#         print(user)
#         if(user is None):
#             if(pw1==pw2):
#                 authenticate(username=un,password=pw1)
#                 return redirect('/login')
#             else:
#                 msg = 'Incorrect password!'
#                 return render(request,'register.html',{'msg':msg})
#         else:
#             msg = 'User already registered!'
#             return render(request,'register.html',{'msg':msg})
#     else:
#         return render(request,'register.html')
   
def profile(request):
    if request.method == "POST" and request.FILES.get('uploadImage'):
        img_name = request.FILES['uploadImage']

        # Save the file using FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(img_name.name, img_name)  # Save image to server
        img_url = fs.url(filename)  # Get the URL of the saved image
        img_path = fs.path(filename)  # Get the full file path for processing

        # Verify if the file is a valid image
        if img_name.content_type not in ['image/jpeg', 'image/png']:
            return render(request, 'profile.html', {'error': 'Invalid file type! Please upload a JPG or PNG image.'})

        # Ensure the image file is readable
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None:
            return render(request, 'profile.html', {'error': 'Error processing the uploaded image. Please try again.'})

        # Resize and prepare the image for prediction
        img = cv2.resize(img, (64, 64))  # Resize image to match model input size
        img = img.flatten()  # Flatten the image for model input
        img = np.expand_dims(img, axis=0)  # Expand dimensions for prediction

        # Predict the disease class using the model
        predict = model.predict(img)[0]

        # Skin disease names and corresponding diagnosis results
        skin_disease_names = ['Athlete Foot', 'Chicken Pox','Shingles' , 'Nail Fungus','Impetigo', 'Cutaneous Larva Migrans', 'Ringworm' ,'Cellulitis']
        diagnosis = ['Athlete foot is a fungal infection that can be treated with antifungal medications and by keeping feet clean and dry.',
                     'The diagnosis and cure for Chickenpox typically involve a combination of self-care, over-the-counter medications, and in some cases, antiviral prescriptions.',
                     'Shingles is caused by the varicella-zoster virus, the same virus that causes chickenpox. There are treatments for shingles symptoms, but there is no cure. There are vaccines against shingles and postherpetic neuralgia.',
                     'Nail fungus, also known as onychomycosis, is a common infection that affects the fingernails or toenails. Diagnosis typically involves a visual examination of the nail, along with a scraping or clipping of the affected nail to examine for fungal elements.',
                     'Impetigo is treated with prescription mupirocin antibiotic ointment or cream applied directly to the sores two to three times a day for five to 10 days.',
                     'Cutaneous Larva Migrans (CLM) is a skin condition caused by the larvae of certain hookworms. The diagnosis typically involves a physical examination and medical history, with a focus on exposure to contaminated soil.',
                     'Ringworm is a fungal infection that affects the skin, hair, and nails. It is not actually caused by a worm, but rather by a type of fungus called a dermatophyte.',
                      'Treatment for cellulitis usually involves antibiotics, and in most cases, you should start to feel better within 7 to 10 days.',
                     ]

        # Check prediction index validity
        if 0 <= predict < len(skin_disease_names):
            result1 = skin_disease_names[predict]
            result2 = diagnosis[predict]
        else:
            result1 = "Unknown"
            result2 = "Unknown"

        # Render the results along with the uploaded image
        return render(request, 'profile.html', {'img_url': img_url, 'obj1': result1, 'obj2': result2})

    # Render the empty profile page for GET requests
    return render(request, 'profile.html')
