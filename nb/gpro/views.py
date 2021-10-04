from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime

def current_datetime(request):
    template = loader.get_template("gpro/index.html")
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(request, '/home/nikolabroyak/GPRO_Web/nb/gpro/templates/gpro/index.html')
