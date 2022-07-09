# Converter

**This app will convert a YouTube video to a downloadable mp3.** <br/>

- Due to resourcing issues, video length is limited to a maximum of 10 minutes, playlist URL is disabled and the resulting mp3 has a bitrate of only 128kbps.<br/>
- Being hosted on **Heroku**, the first time you use it may take a little bit longer.<br/>

The app uses:<br/>
**youtube-dl** for extracting video info and downloading the video,<br/>
**ffmpeg** to extract audio from videofile,<br/>
**Celery** for asynchronous tasks with **RabbitMQ** for broker,<br/>
**PostgreSQL** for db and **AWS S3** for storage.<br/>