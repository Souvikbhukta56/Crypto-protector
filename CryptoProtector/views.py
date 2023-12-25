from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse
from django.conf import settings
import json
import requests
import os
from shutil import rmtree
from passlib.hash import bcrypt
from AES import AES
from db import DB

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirmpass = request.POST.get('password2')
        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters')
        elif password == confirmpass:
            try:
                hashed_password = bcrypt.hash(password)
                DB.save_user_data(uname, email, hashed_password) # Stores into MySQL 
            except Exception:
                messages.error(request, 'Username or email already exists')
                return redirect('signup')
            messages.success(request, 'Signup successful')
            return redirect('login')
    return render(request,"signup.html")

def login(request):
    if request.session.get('user_authenticated'):
        return redirect('share-file')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        if DB.authenticate(username, password):
            request.session['user_authenticated'] = True
            request.session['current_user'] = username
            return redirect('share-file')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request,'Login.html')

def logout(request):
    request.session.clear()
    return redirect('login')

def store_json_data(data):
    data = {"data": json.dumps(data)}
    headers = {"Content-Type": "application/json", "X-Master-Key": settings.JSONBIN_API_KEY}
    response = requests.post(settings.JSONBIN_API_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['metadata']['id'] # bin id
    else:
        print(response.json().get('message', 'Unknown error'))
        return False

def share_file(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    if request.method == 'POST' and request.FILES['fileToUpload']:
        receiver = request.POST.get('name')
        file = request.FILES['fileToUpload']
        ciphertext = AES().encrypt(file.read())
        bin_id = store_json_data(ciphertext) # Storing encrypted data into jsonbin.io
        if bin_id:
            DB.save_file(bin_id, request.session['current_user'], receiver, file.name) # Storing file details into MySQL
            messages.success(request, 'File send successfully!')
            return redirect('share-file')
    return render(request,'Share_file.html', {'users': DB.get_usernames()})

def received_files(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    data = DB.show_files(request.session['current_user']) # Getting list of file details
    return render(request,'Received_files.html', {'items': data})

def retrieve_json_data(bin_id):
    api_url = f"{settings.JSONBIN_API_ENDPOINT}/{bin_id}"
    headers = {"Content-Type": "application/json", "X-Master-Key": settings.JSONBIN_API_KEY}
    response = requests.get(api_url, headers=headers)
    try:
        json_data = response.json()['record']['data']
        return json.loads(json_data)
    except Exception:
        return False
    

def download_file(request, file_id):
    try:
        if not request.session.get('user_authenticated'):
            return redirect('login')
        if os.path.exists("temp"):
            rmtree("temp")
        file_name = DB.get_file_name(file_id)
        ciphertext = retrieve_json_data(file_id)
        if ciphertext == False:
            messages.error(request, 'File not found')
            return redirect('received-files')
        AES().decrypt(ciphertext, file_name)
        if request.method == 'POST':
            file = open("./temp/"+file_name, 'rb')
            response = FileResponse(file, as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except Exception:
        messages.error(request, "Something went wrong")
    return render(request, 'Download_file.html', {'file_name': file_name})
