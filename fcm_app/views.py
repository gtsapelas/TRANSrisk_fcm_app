from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .forms import FCMForm
from .models import FCM
from django.http import HttpResponse
from django.contrib import messages
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    context = {'a_var': "no_value"}
    return render(request, 'fcm_app/index.html', context)


def browse(request):
    all_fcms = FCM.objects.all()
    paginator = Paginator(all_fcms, 6)
    page = request.GET.get('page')
    try:
        all_fcms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_fcms = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_fcms = paginator.page(paginator.num_pages)
    return render(request, 'fcm_app/browse.html', {"all_fcms": all_fcms})


def import_fcm(request):
    if request.method == 'POST':
        form = FCMForm(request.POST, request.FILES)
        if form.is_valid():
            print request.user
            fcm = FCM(user=request.user,
                      title=form.cleaned_data['title'],
                      description=form.cleaned_data['description'],
                      creation_date=datetime.now(),
                      map_image=form.cleaned_data['map_image'],
                      map_html=form.cleaned_data['map_html'])
            fcm.save()
            messages.success(request, 'FCM imported successfully')
    form = FCMForm()
    return render(request, 'fcm_app/import_fcm.html', {
        'form': form
    })


def view_fcm(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    html = fcm.map_html.read()
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body').prettify().replace('<body>', '').replace('</body>', '')
    src = [x['src'] for x in soup.findAll('img')][0]
    body = body.replace('src="' + src + '"', 'src="' + fcm.map_image.url + '" width="100%" class="img-responsive"')
    body = body.replace('showTooltip', 'showTooltip2')
    script = soup.find('script').prettify()
    return render(request, 'fcm_app/view_fcm.html', {
        'map_body': body,
        'map_image': fcm.map_image,
        'script': script,
        'fcm': fcm,
    })
