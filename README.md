# Converter

**A Django app that allows users to convert Youtube videos to audio files that can be downloaded.** 
  
  Previous app version was hosted on Heroku, now looking for free alternatives.<br/><br/>


## Technical Details

  * Built on Django, a popular web framework for building web applications using Python.
  * Utilizes **Celery** for asynchronous task management, with **RabbitMQ** as a message broker to handle communication between Celery workers.
  * **Celery Progress Bar** to display progress/info on the current running task.
  * Incorporates **AJAX** requests that allows the page to update asynchronously by exchanging data to and from the server.
  * Uses **youtube-dl** for extracting video info and **ffmpeg** to extract audio from videofile.<br/><br/>

## Features

  * Minimalistic and intuitive interface.
  * Quality and format select options.
  * Background image and progress bar for entertainment purposes.<br/><br/>

## Preview

![Screenshot](https://github.com/vio-m/Converter/blob/master/static/img/Screenshot%20from%202023-01-24%2012-02-58.png) 
![Screenshot](https://github.com/vio-m/Converter/blob/master/static/img/Screenshot%20from%202023-01-24%2012-03-17.png) 
![Screenshot](https://github.com/vio-m/Converter/blob/master/static/img/Screenshot%20from%202023-01-24%2012-03-35.png)
![Screenshot](https://github.com/vio-m/Converter/blob/master/static/img/Screenshot%20from%202023-01-24%2012-03-46.png)


