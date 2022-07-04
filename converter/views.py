from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.generic import View
from .models import Video
from .forms import urlForm
from .validator import url_is_valid
from .tasks import get_info, get_audio
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
import time
import json


class GenericView(View):
    def get(self, request):
        if request.method == "GET":
            return render(request, 'main.html')

    def post(self, request):
        if request.is_ajax and request.method == 'POST':
            form = urlForm(request.POST)
            if form.is_valid():
                video_url = form.cleaned_data['url']
                if url_is_valid(video_url):
                    try:
                        info_dict = get_info(video_url)
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


def convert(request):
    form = urlForm(request.POST)
    if request.is_ajax and request.method == 'POST':
        if form.is_valid():
            video_url = form.cleaned_data['url']
            task = get_audio.delay(video_url)
            task_id = task.task_id
            result = AsyncResult(task_id)
            context = {'task_id': result.id}
            #result.get(timeout=60)
            #while result.ready() == False:
            #    time.sleep(0.5)
            #print('>>>CONVERTED WITH:', result.status)
            result.forget()
            return JsonResponse(context, status=200)
        else:
            context = {"error": '>>> form is not valid'}
            return JsonResponse(context, status=400)
    else:
        context = {"error": form.errors.as_data()}
        return JsonResponse(context, status=400)




