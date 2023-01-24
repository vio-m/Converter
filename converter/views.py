import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core import serializers
from django.views.generic import View
from .models import Video
from .forms import urlForm, convertForm, titleForm
from .validator import url_is_valid
from .tasks import get_info, get_audio, wait_and_delete
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
import time
import json




class GenericView(View):
    model = Video
    def get(self, request):
        if request.method == "GET":
            return render(request, 'main.html')

    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            form = urlForm(request.POST)
            if form.is_valid():
                video_url = form.cleaned_data['url']
                if url_is_valid(video_url):
                    try:
                        info_dict = get_info(video_url)
                        context = {"title": info_dict['video_title'],
                                   "thumb": info_dict['thumbnail'],
                                   "url": video_url}

                        title = context['title']
                        typ = form.cleaned_data['format']
                        new_entry = Video.objects.create(title=title, typ=typ, url=video_url)
                        new_entry.save()

                        if info_dict['duration'] > 600:
                            context = {"error": 'Video is over 10 min. Try shorter clips!'}
                            new_entry.delete()
                            return JsonResponse(context, status=413)
                        return JsonResponse(context, status=200)
                    except Exception as e:
                        context = {"error": e}
                        return JsonResponse(context, status=400)
                else:
                    context = {"error": 'Invalid URL. Try again!'}
                    return JsonResponse(context, status=400)
            else:
                context = {"error": form.errors.as_data()}
                return JsonResponse(context, status=400)
        else:
            form = urlForm()


def convert(request):
    form = convertForm(request.POST)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        if form.is_valid():
            video_url = form.cleaned_data['url']
            qlt = form.cleaned_data['quality']
            typ = form.cleaned_data['format']
            task = get_audio.delay(video_url, qlt, typ)
            task_id = task.task_id
            result = AsyncResult(task_id)
            context = {'task_id': result.id}
            result.forget()
            return JsonResponse(context, status=200)
        else:
            context = {"error": "Form is not valid !"}
            return JsonResponse(context, status=400)
    else:
        context = {"error": form.errors.as_data()}
        return JsonResponse(context, status=400)


def download_and_delete(request):
    form = titleForm(request.POST)
    title = form['title'].value()
    obj = Video.objects.filter(title=title).first()

    if obj != None:
        filename = obj.title + "." + obj.typ
        file_path = "static/media/" + filename
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/download'#'audio/mpeg'
        response['Content-Disposition'] = 'attachment; filename='+filename
        response['Content-Length'] = os.path.getsize(file_path)
        response['Custom-Filepath'] = file_path
        try:
            obj.delete()
            wait_and_delete.delay(filename)
            return response
        except Exception as e:
            context = {"error": e}
            return JsonResponse(context, status=400)


            #if os.path.exists("static/media/" + filename):
                #pass
                #time.sleep(10)
                #obj.delete()
                #os.remove("static/media/" + filename)




'''


Here is an example of a Django view function that can be used to return a file for download:

from django.http import FileResponse

def download_file(request):
    # specify the file path
    file_path = '/path/to/file.pdf'

    # create a FileResponse object
    response = FileResponse(open(file_path, 'rb'))

    # set the content type and the content disposition headers
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'

    return response

---------------------

def download(request):
    filename = "M1 Abrams deja vu.mp3"
    with open("static/media/M1 Abrams deja vu.mp3", "rb") as fl:
        datafile = fl.read()
        response = FileResponse(datafile, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename=M1 Abrams deja vu.mp3'
        delete(filename)
        return response

--------------------

class GenericView(View):
    def get(self, request):
        if request.method == "GET":
            return render(request, 'main.html')

    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            form = urlForm(request.POST)
            if form.is_valid():
                video_url = form.cleaned_data['url']
                #video_bitrate = form.cleaned_data['quality']
                if url_is_valid(video_url):
                    try:
                        info_dict = get_info(video_url) #, video_bitrate
                        context = {"title": info_dict['video_title'],
                                   "thumb": info_dict['thumbnail'],
                                   "url": video_url}
                        if info_dict['duration'] > 600:
                            context = {"error": '>>> Video is over 10 min. Try shorter clips!'}
                            return JsonResponse(context, status=413)
                        return JsonResponse(context, status=200)
                    except Exception as e:
                        context = {"error": e}
                        return JsonResponse(context, status=400)
                else:
                    context = {"error": '>>> The URL is not valid. Try again!'}
                    return JsonResponse(context, status=400)
            else:
                context = {"error": form.errors.as_data()}
                return JsonResponse(context, status=400)
        else:
            form = urlForm()


    def convert(request, video_url):
        task = get_audio.delay(video_url)
        task_id = task.task_id
        result = AsyncResult(task_id)
        context = {'task_id': result.id}
        result.forget()
        with open("static/media/M0.mp3", "rb") as fl:
            response = FileResponse(fl.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename=M0.mp3'
            print("response: ", response)
            return response

------------------------------------------------------

    form = urlForm(request.POST)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        if form.is_valid():
            fl = open("static/media/M0.mp3", "r")
            response = HttpResponse(fl, content_type='audio/mpeg')
            response['Content-Disposition'] = 'inline; filename=M0.mp3'
            
            video_url = form.cleaned_data['url']
            
            task = get_audio.delay(video_url)
            task_id = task.task_id
            result = AsyncResult(task_id)
            context = {'task_id': result.id}
            result.forget() 
            
            #result.get(timeout=60)
            #while result.ready() == False:
            #    time.sleep(0.5)
            #print('>>>CONVERTED WITH:', result.status)
                       
            return response #, JsonResponse(context, status=200)
        else:
            context = {"error": "Form is not valid !"}
            return JsonResponse(context, status=400)
    else:
        context = {"error": form.errors.as_data()}
        return JsonResponse(context, status=400)
'''



