from django.shortcuts import render
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
import requests, os
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .models import Object
from .forms import ObjectForm
import logging




def generate_token(request, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}
    data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
    r = requests.post(url, headers=headers, data=data)
    headers = r.headers.get('X-Subject-Token')
    return render(request, 'files/success.html', {'header': headers})


@api_view(['GET', 'PUT'])
def container_list(request,account, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}

    if (account == "swift"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
    elif (account == "openedx"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
    elif (account == "telemet") :
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"

    r = requests.post(url, headers=headers, data=data)
    token = r.headers.get('X-Subject-Token')
    if request.method == 'GET':
        r = requests.get('http://10.129.103.86:8080/v1/'+acc+'/', headers={'X-Auth-Token': token}).text
        return Response (r)


    if request.method == 'PUT':
        data = JSONParser().parse(request)
        #new_cont = request.data
        new_cont = data["name"]
        r = requests.put('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + new_cont,
                         headers={'X-Auth-Token': token}).text
        return Response(r)

@api_view (['GET'])
def metadata (request, account, container, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}
    if (account == "swift"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
    elif (account == "openedx"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
    else:
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"
    r = requests.post(url, headers=headers, data=data)
    token = r.headers.get('X-Subject-Token')
    if request.method == 'GET':
        r = requests.get('http://10.129.103.86:8080/v1/'+ acc +'/' + container,
                         headers={'X-Auth-Token': token})
        return Response (r.headers)

@api_view(['GET', 'DELETE', 'POST'])
def object_list(request, account, container, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}
    if (account == "swift"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
    elif (account == "openedx"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
    else:
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"
    r = requests.post(url, headers=headers, data=data)
    token = r.headers.get('X-Subject-Token')

    if request.method == 'GET':
        r = requests.get('http://10.129.103.86:8080/v1/'+ acc +'/' + container,
                         headers={'X-Auth-Token': token}).text
        return Response (r)


    if request.method == 'DELETE':
        r = requests.delete('http://10.129.103.86:8080/v1/'+ acc +'/' + container,
                            headers={'X-Auth-Token': token}).text
        return Response("Successfully Deleted Container")
    if request.method == 'POST':
        t = {'X-Auth-Token': token }
        print(request.body)
        data = JSONParser().parse(request)

        data.update (t)
        requests.post('http://10.129.103.86:8080/v1/'+ acc +'/' + container,headers=data)
        r = requests.get('http://10.129.103.86:8080/v1/'+ acc +'/' + container,
                         headers={'X-Auth-Token': token})
        return Response (r.headers)


@api_view(['GET', 'DELETE', 'POST'])
def object_details (request,account, container, object, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}
    if (account == "swift"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
    elif (account == "openedx"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
    else:
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"
    r = requests.post(url, headers=headers, data=data)

    token = r.headers.get('X-Subject-Token')
    if request.method == 'GET':
        r = requests.get('http://10.129.103.86:8080/v1/'+ acc +'/' + container + '/' + object,
            headers={'X-Auth-Token': token})

        return Response (r.headers)
    if request.method == 'POST':
        t = {'X-Auth-Token': token}
        data = JSONParser().parse(request)
        data.update(t)
        requests.post('http://10.129.103.86:8080/v1/'+ acc +'/' + container + '/' + object,
                      headers=data)
        r = requests.get(
            'http://10.129.103.86:8080/v1/'+ acc +'/' + container + '/' + object,
            headers={'X-Auth-Token': token})
        return Response(r.headers)

    if request.method == 'DELETE':
        r = requests.delete(
            'http://10.129.103.86:8080/v1/'+ acc +'/' + container + '/' + object,
            headers={'X-Auth-Token': token}).text
        return Response("Successfully Deleted Object")


@api_view(['GET'])
def download_object(request, account, container, object, format=None):
    url = 'http://10.129.103.86:5000/v3/auth/tokens'
    headers = {'content-type': 'application/json'}
    if (account == "swift"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
    elif (account == "openedx"):
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
    else:
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"
    r = requests.post(url, headers=headers, data=data)
    token = r.headers.get('X-Subject-Token')
    if request.method == 'GET':
        r = requests.get(
            'http://10.129.103.86:8080/v1/' + acc + '/' + container + '/' + object,
            headers={'X-Auth-Token': token}).content

        name,ext = os.path.splitext(object)

        # ext = ext.lower()
        if (ext == ".png"):
            return HttpResponse(r, 'image/png')
        elif (ext == ".PNG"):
            return HttpResponse(r, 'image/PNG')
        elif (ext == ".jpeg" or ext == ".jpg"):
            return HttpResponse(r, 'image/jpeg')
        elif (ext == ".txt"):
            return HttpResponse(r, 'text/plain')
        elif(ext == ".pdf"):
            return HttpResponse (r, 'application/pdf')
        elif(ext == ".zip"):
            return HttpResponse(r, 'application/zip')
        elif (ext == ".mp4"):
            return HttpResponse(r, 'audio/mp4')
        elif (ext == ".mp3"):
            return HttpResponse(r, 'audio/basic')
        elif (ext == ".csv"):
            return HttpResponse(r, 'text/csv')
        else:
            return Response("Format Not Supported!")



@api_view (['GET', 'POST'])
def upload (request,account, container, format=None):
    print(request.META)
    print (request)
    print (request.FILES)
    form = ObjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        a = form.save(commit=False)
        a.file = request.FILES['file']
        name, ext = os.path.splitext(a.file.name)
        ext = ext.lower()
        if (ext == ".csv" or ext == ".png" or ext == ".jpeg" or ext == ".jpg" or ext == ".mp4" or ext == ".mp3" or ext == ".pdf" or ext == ".zip" or ext == ".txt"):
            a.save()
            url = 'http://10.129.103.86:5000/v3/auth/tokens'
            headers = {'content-type': 'application/json'}
            if (account == "swift"):
                data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
                acc = "AUTH_b3f70be8acad4ec197e2b5edf48d9e5a"
            elif (account == "openedx"):
                data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "openedx",\n          "domain": { "name": "default" },\n          "password": "openedx"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "openedx",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
                acc = "AUTH_081223a854f54e37a0d6a1c383c5577e"
            else:
                data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "telemet",\n          "domain": { "name": "default" },\n          "password": "telemet"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "datastore",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
                acc = "AUTH_5b2bcbcb10f347aaa4c7b0e370c2c055"
            r = requests.post(url, headers=headers, data=data)
            token = r.headers.get('X-Subject-Token')
            path = "C:/Users/ARUSHI/Desktop/swift2/media/"+a.file.name

            s = requests.put('http://10.129.103.86:8080/v1/'+ acc +'/' + container + '/' + a.file.name,
                             headers={'X-Auth-Token': token}, data=open(path, "rb")).text
            os.remove(path)

            #print(request.META)
            return Response("Successfully Uploaded")
        else:
            return Response ("Format not supported. Supported formats include png, jpeg, mp3, mp4, zip, pdf, txt. For all other files, create a zip file and try again!")
    context = {
        "form": form,
    }
    #print(request.META)
    print("Incorrect")
    return Response ("The form isn't filled properly")
    #return render(request, 'files/input.html', context)

