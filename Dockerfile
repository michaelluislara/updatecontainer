FROM python:bullseye
COPY ../ .
RUN pip install pandas
# RUN pip install shapely
RUN pip install geopandas
RUN pip install gunicorn
# RUN ["chmod", "+x", "commands.sh"]
RUN ["chmod", "+x", "downloader.py"]
RUN ["chmod", "+x", "test.py"]
RUN ["chmod", "+rwx", "tracker.txt"]
RUN useradd mike
RUN apt-get update
# RUN apt-get -y install cron
# COPY example-crontab /etc/cron.d/example-crontab
# COPY cron.allow /etc/cron.allow
# RUN chmod a+rwx /etc/cron.d/example-crontab && crontab /etc/cron.d/example-crontab
RUN chmod a+rwx downloadertracker.txt
RUN chmod a+rwx commands.sh
# RUN chmod a+rwx /var/run/crond.pid
# RUN service cron start
# EXPOSE 8000
USER mike
# # RUN pip install -r requirements.txt
# CMD ["Python", "download.py"]
# CMD python downloader.py
CMD bash commands.sh
# ENTRYPOINT ["gunicorn" , "--bind", "0.0.0.0:8000", "app:app"]
# CMD [ "gunicorn", "app:app" ]