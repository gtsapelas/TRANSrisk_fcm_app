from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .forms import FCMForm,FCMCONCEPTForm
from .models import FCM
from .models import FCM_CONCEPT
from .models import FCM_CONCEPT_INFO
from django.http import HttpResponse
from django.contrib import messages
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from django import forms


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
            user = request.user
            if user.is_authenticated():
                fcm = FCM(user=user,
                          title=form.cleaned_data['title'],
                          description=form.cleaned_data['description'],
                          creation_date=datetime.now(),
                          map_image=form.cleaned_data['map_image'],
                          map_html=form.cleaned_data['map_html'])
                fcm.save()
                soup = BeautifulSoup(fcm.map_html, "html.parser")  # vazo i lxml  i html.parser
                x = soup.findAll("div", class_="tooltip")
                for div in x:
                    fcm_concept = FCM_CONCEPT(fcmname=fcm, title=div.text)
                    fcm_concept.save()
                messages.success(request, 'FCM imported successfully! '
                                          'You can edit the concepts <a href="/fcm/view-fcm-concept/' + str(fcm.pk) + '"><u>here</u></a>')
            else:
                messages.error(request, "You must login to import a map")
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


def view_fcm_concept(request, fcm_id):
    concepts = FCM_CONCEPT.objects.filter(fcmname=fcm_id)   # den ksero mipos prepei na ginei get anti gia filter
    return render(request, 'fcm_app/view_fcm_concept.html', {"fcm_id": fcm_id, "concepts": concepts})


def view_fcm_concept_info(request, fcm_id, concept_id):
    if request.method == 'POST':
        form = FCMCONCEPTForm(request.POST)
        if form.is_valid():
            my_concept = get_object_or_404(FCM_CONCEPT, pk=concept_id)
            fcm_concept_info = FCM_CONCEPT_INFO(fcm_concept=my_concept, info=form.cleaned_data['information_text'])
            fcm_concept_info.save()
    form = FCMCONCEPTForm()
    concept = FCM_CONCEPT.objects.get(fcmname=fcm_id, pk=concept_id)
    return render(request, 'fcm_app/view_fcm_concept_info.html/', {
        'form': form, 'concept': concept,
    })


def my_fcms(request):
    my_fcms = []
    user = request.user
    if user.is_authenticated():
        my_fcms = FCM.objects.filter(user=user)
    return render(request, 'fcm_app/my_fcms.html/', {
        'my_fcms': my_fcms,
    })


def edit_fcm(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    if request.method == 'POST':
        data = {'map_image': fcm.map_image, 'map_html': fcm.map_html}
        form = FCMForm(request.POST, data)
        if form.is_valid():
            print request.user
            user = request.user
            if user.is_authenticated():
                fcm.title=form.cleaned_data['title']
                fcm.description=form.cleaned_data['description']
                fcm.save()

                messages.success(request, 'edited successfully')
            else:
                messages.error(request, "You must login to edit a map")
        else:
            messages.error(request, "form invalid")
    data = {'title': fcm.title, 'description': fcm.description}
    form = FCMForm(initial=data)
    form.fields['map_image'].widget = forms.HiddenInput()
    form.fields['map_html'].widget = forms.HiddenInput()

    return render(request, 'fcm_app/edit_fcm.html', {
        'form': form,
        'fcm': fcm,
    })
