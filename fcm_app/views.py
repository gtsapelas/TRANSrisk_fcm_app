from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import jsForm, FCMForm,FCMCONCEPTForm, FiltersForm, chartisForm
from .models import FCM
from .models import FCM_CONCEPT
from .models import FCM_CONCEPT_INFO
from . models import Tags
#from .models import mynew
from .models import FCM_EDGES
from django.http import HttpResponse
from django.contrib import messages
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from django import forms
import json, pdb

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    context = {'a_var': "no_value"}
    return render(request, 'fcm_app/index.html', context)


def browse(request):

    if request.method == 'POST':
        filter_form = FiltersForm(request.POST)
        if filter_form.is_valid():
            filtered_title_and_or_description = filter_form.cleaned_data['filtered_title_and_or_description']
            filtered_year = filter_form.cleaned_data['filtered_year']
            filtered_country = filter_form.cleaned_data['filtered_country']
            filtered_getmine = filter_form.cleaned_data['filtered_getmine']
            filtered_tags = filter_form.cleaned_data['filtered_tags']
            if request.user.is_authenticated:
                all_fcms = FCM.objects.filter(Q(status='1') | Q(user=request.user)).order_by('creation_date').reverse()
            else:
                all_fcms = FCM.objects.filter(Q(status='1')).order_by('creation_date').reverse()
            if filtered_year != "-":
                all_fcms = all_fcms.filter(creation_date__year=filtered_year)
            if filtered_country != "-":
                all_fcms = all_fcms.filter(country=filtered_country)
            all_fcms = all_fcms.filter(Q(title__icontains=filtered_title_and_or_description) | Q(
                description__icontains=filtered_title_and_or_description)).distinct()

            if filtered_tags:
                queryset_list = []
                for element in filtered_tags:
                    try:
                        queryset_list.append(Tags.objects.get(pk=str(element)).fcm_set.all())
                    except DatabaseError:
                        pass
                    except ObjectDoesNotExist:
                        pass

                results_union = FCM.objects.none()
                for q in queryset_list:
                    results_union = (results_union | q )
                results_union = results_union.distinct()
                all_fcms = results_union & all_fcms

            if 'filtered_getmine' in request.POST:  #check if the checkbox is checked or not
                filtered_getmine = request.POST['filtered_getmine']
            else:
                filtered_getmine = False
            if filtered_getmine:
                all_fcms = all_fcms.filter(manual='1')
            data = {'filtered_title_and_or_description': filtered_title_and_or_description, 'filtered_year': filtered_year, 'filtered_country': filtered_country, 'filtered_getmine': filtered_getmine,'filtered_tags': filtered_tags}
            filter_form = FiltersForm(initial=data)
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
            return render(request, 'fcm_app/browse.html',
                          {"all_fcms": all_fcms, "filter_form": filter_form, "filter_tags":filtered_tags})


    #all_fcms = FCM.objects.all()
    if request.user.is_authenticated:
        all_fcms = FCM.objects.filter(Q(status='1') | Q(user=request.user)).order_by('creation_date').reverse()
    else:
        all_fcms = FCM.objects.filter(Q(status='1')).order_by('creation_date').reverse()
    filter_form = FiltersForm()
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
    return render(request, 'fcm_app/browse.html', {"all_fcms": all_fcms, "filter_form": filter_form})


@login_required
def import_fcm(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = FCMForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.user)
            user = request.user
            if user.is_authenticated():
                fcm = FCM(user=user,
                          title=form.cleaned_data['title'],
                          country = form.cleaned_data['country'],
                          status = form.cleaned_data['status'],
                          description=form.cleaned_data['description'],
                          creation_date=datetime.now(),
                          map_image=form.cleaned_data['map_image'],
                          map_html=form.cleaned_data['map_html'])
                fcm.save()
                tags = form.cleaned_data['tags']
                for tag_element in tags:
                    try:
                        new_tag = Tags(name=str(tag_element))
                        new_tag.save()
                    except DatabaseError:
                        pass
                    fcm.tags.add(str(tag_element))
                soup = BeautifulSoup(fcm.map_html, "html.parser")  # vazo i lxml  i html.parser
                x = soup.findAll("div", class_="tooltip")
                for div in x:
                    fcm_concept = FCM_CONCEPT(fcm=fcm, title=div.text, id_in_fcm=div.get('id'))
                    fcm_concept.save()
                messages.success(request, 'Successfully imported the System Map. Edit the Map <a href="/fcm/view-fcm-concept/' + str(fcm.id) + '/"><u>here</u></a>, or you can browse the rest of the Maps <a href="/fcm/browse"><u>here</u></a>. ')
            else:
                messages.error(request, "You must login to import a map")
    form = FCMForm()
    return render(request, 'fcm_app/import_fcm.html', {
        'form': form
    })


def view_fcm(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    if fcm.manual == False:
        html = fcm.map_html.read()
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body').prettify().replace('<body>', '').replace('</body>', '')
        src = [x['src'] for x in soup.findAll('img')][0]
        # body = body.replace('src="' + src + '"', 'src="' + fcm.map_image.url + '" width="100%" class="img-responsive"') #<--ayto xalaei to area highlight
        body = body.replace('src="' + src + '"', 'src="' + fcm.map_image.url + '" ')
        body = body.replace('onmouseover="showTooltip(', 'onclick="showTooltip2(event, ')
        body = body.replace('document.onmousemove = updateTooltip;', '')
        # body = body.replace('shape="rect"', 'shape="rect" data-toggle="popover" data-content="Some content"')
        script = soup.find('script').prettify()

        concepts = FCM_CONCEPT.objects.filter(fcm=fcm)
        print(concepts)
        info_dict = dict()
        for concepts_item in concepts:
            try:
                concept_info = FCM_CONCEPT_INFO.objects.get(fcm_concept=concepts_item)
                info_dict[str(concepts_item.id_in_fcm)] = concept_info.info
            except FCM_CONCEPT_INFO.DoesNotExist:
                info_dict[str(concepts_item.id_in_fcm)] = 'No information available'
        print(info_dict)

        return render(request, 'fcm_app/view_fcm.html', {
            'map_body': body,
            'map_image': fcm.map_image,
            'script': script,
            'fcm': fcm,
            'info_dict': info_dict
        })
    else:
        x = fcm.chartis  # tha exo to string, pou tha pernao sto html gia na to deihno
        #data = {'title': "fd", 'description': x}
        #form = jsForm(data)
        concepts = FCM_CONCEPT.objects.filter(fcm=fcm)
        print(concepts)
        info_dict = dict()
        for concepts_item in concepts:
            try:
                concept_info = FCM_CONCEPT_INFO.objects.get(fcm_concept=concepts_item)
                info_dict[str(concepts_item.id_in_fcm)] = concept_info.info
            except FCM_CONCEPT_INFO.DoesNotExist:
                info_dict[str(concepts_item.id_in_fcm)] = 'No information available'
        print(info_dict)
        return render(request, 'fcm_app/view_fcm4.html', {
            'fcm': fcm,
            #'data1': x,
            #'form': form,
            'info_dict': info_dict
        })



def delete_fcm(request, fcm_id):
    FCM.objects.get(pk=fcm_id).delete()
    return render(request, 'fcm_app/index.html', {})


@login_required
def view_fcm_concept(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    if request.user == fcm.user:
        concepts = FCM_CONCEPT.objects.filter(fcm=fcm_id)   # den ksero mipos prepei na ginei get anti gia filter
        return render(request, 'fcm_app/view_fcm_concept.html', {"fcm_id": fcm_id, "concepts": concepts})
    return HttpResponseForbidden()

@login_required
def view_fcm_concept_info(request, fcm_id, concept_id):
    storage = messages.get_messages(request)
    storage.used = True
    fcm = FCM.objects.get(pk=fcm_id)
    if request.user == fcm.user:
        concept = FCM_CONCEPT.objects.get(fcm=fcm_id, pk=concept_id)
        concept_info = FCM_CONCEPT_INFO()
        try:
            concept_info = FCM_CONCEPT_INFO.objects.get(fcm_concept=concept_id)
            data = {'concept_info': concept_info.info}
        except concept_info.DoesNotExist:
            data = {}

        form = FCMCONCEPTForm(initial=data)
        if request.method == 'POST':
            form = FCMCONCEPTForm(request.POST)
            if form.is_valid():
                my_concept = get_object_or_404(FCM_CONCEPT, pk=concept_id)
                fcm_concept_info = FCM_CONCEPT_INFO()
                try:
                    fcm_concept_info = FCM_CONCEPT_INFO.objects.get(fcm_concept=my_concept)
                    fcm_concept_info.info = form.cleaned_data['concept_info']
                except fcm_concept_info.DoesNotExist:
                    fcm_concept_info = FCM_CONCEPT_INFO(fcm_concept=my_concept, info=form.cleaned_data['concept_info'])
                fcm_concept_info.save()
                messages.success(request, 'edited successfully')
            else:
                messages.error(request, "an error occured")
        return render(request, 'fcm_app/view_fcm_concept_info.html/', {
            'form': form, 'concept': concept,
        })
    return HttpResponseForbidden()

@login_required
def my_fcms(request):
    my_fcms = []
    user = request.user
    if user.is_authenticated():
        my_fcms = FCM.objects.filter(user=user)
    return render(request, 'fcm_app/my_fcms.html/', {
        'my_fcms': my_fcms,
    })

@login_required
def edit_fcm(request, fcm_id):
    storage = messages.get_messages(request)
    storage.used = True

    fcm = FCM.objects.get(pk=fcm_id)
    if fcm.manual == False:
        if request.user == fcm.user:
            if request.method == 'POST':
                data = {'map_image': fcm.map_image, 'map_html': fcm.map_html}
                form = FCMForm(request.POST, data)
                if form.is_valid():
                    print(request.user)
                    user = request.user
                    if user.is_authenticated():
                        fcm.title=form.cleaned_data['title']
                        fcm.description=form.cleaned_data['description']
                        fcm.country=form.cleaned_data['country']
                        fcm.status=form.cleaned_data['status']
                        fcm.save()
                        tags = form.cleaned_data['tags']
                        fcm.tags.clear()

                        for tag_element in tags:
                            try:
                                new_tag = Tags(name=str(tag_element))
                                new_tag.save()
                            except DatabaseError:
                                pass
                            fcm.tags.add(str(tag_element))

                        messages.success(request, 'edited successfully')
                    else:
                        messages.error(request, "You must login to edit a map")
                else:
                    messages.error(request, "form invalid")
            data = {'title': fcm.title, 'description': fcm.description, 'country': fcm.country, 'status': fcm.status}
            form = FCMForm(initial=data)
            form.fields['map_image'].widget = forms.HiddenInput()
            form.fields['map_html'].widget = forms.HiddenInput()

            return render(request, 'fcm_app/edit_fcm.html', {
                'form': form,
                'fcm': fcm,
            })
        return HttpResponseForbidden()
    else:
        if request.user == fcm.user:
            if request.method == 'POST':
                #data = {'map_image': fcm.map_image, 'map_html': fcm.map_html}
                #data = {'chartis': fcm.chartis}
                #print(data)
                form = jsForm(request.POST)
                form1 = chartisForm(request.POST)
                if form.is_valid():
                    print(request.user)
                    user = request.user
                    if user.is_authenticated():
                        fcm.title=form.cleaned_data['title']
                        fcm.description=form.cleaned_data['description']
                        fcm.country=form.cleaned_data['country']
                        fcm.status=form.cleaned_data['status']
                        fcm.chartis = form.cleaned_data['chartis']
                        fcm.save()
                        tags = form.cleaned_data['tags']
                        fcm.tags.clear()
                        for tag_element in tags:
                            try:
                                new_tag = Tags(name=str(tag_element))
                                new_tag.save()
                            except DatabaseError:
                                pass
                            fcm.tags.add(str(tag_element))
                        if form1.is_valid():
                            arxikos_chartis = json.loads(form1.cleaned_data['arxikos_chartis'])
                        #print(arxikos_chartis)
                        telikos_chartis = json.loads(form.cleaned_data['chartis'])

                        #print(telikos_chartis)

                        x1 = arxikos_chartis['nodes']  # list pou exei dictionaries
                        x2 = telikos_chartis['nodes']
                        arr1 = []
                        arr2 = []

                        for i in x1:
                            arr1.append(i['id'])
                        for i in x2:
                            arr2.append(i['id'])

                        for val in arr1:   # edo pairno tous komvous pou prepei na diagrapso
                            if val not in arr2:
                                b = FCM_CONCEPT.objects.filter(fcm_id=fcm.id, id_in_fcm=val)
                                b.delete()

                        komvoi = []
                        for i in arr2:  # vazo ston pinaka komvoi tous komvous pou prosthethikan
                            if i not in arr1:
                                komvoi.append(x2[next((index for (index, d) in enumerate(x2) if d['id'] == i), None)])

                        for i in komvoi:  # edo tous prostheto sti vasi
                            fcm_concept = FCM_CONCEPT(fcm=fcm, title=i['label'], id_in_fcm=i['id'], x_position=i['x'],y_position=i['y'])
                            fcm_concept.save()

                        b = FCM_CONCEPT.objects.filter(fcm_id=fcm.id) # pairno edo olous tous komvous pou yparhoun pleon
                        j=0
                        for i in b:  # edo kano update se kathe fcm_concept pou einai sti vasi ta parakato stoixeia
                            i.title = x2[j]['label']
                            i.x_position = x2[j]['x']
                            i.y_position = x2[j]['y']
                            j += 1
                            i.save()

                        # antistoixa gia tis akmes
                        x1 = arxikos_chartis['edges']
                        print(x1)
                        x2 = telikos_chartis['edges']
                        print(x2)
                        arr1 = []
                        arr2 = []

                        for i in x1:
                            arr1.append(i['id'])
                        for i in x2:
                            arr2.append(i['id'])

                        b=[]
                        for val in arr1:   # edo pairno tis akmes pou prepei na diagrapso
                            if val not in arr2:
                                b = FCM_EDGES.objects.filter(fcm_id=fcm.id, id_in_fcm_edges=val)
                                b.delete()

                        akmes = []
                        for i in arr2:  # vazo ston pinaka akmes tis akmes pou prosthethikan
                            if i not in arr1:
                                akmes.append(x2[next((index for (index, d) in enumerate(x2) if d['id'] == i), None)])

                        for i in akmes:  # edo tis prostheto sti vasi
                            fcm_edge = FCM_EDGES(fcm=fcm, title=i['label'], id_in_fcm_edges=i['id'], from_node=i['from'], to_node=i['to'])
                            fcm_edge.save()

                        c = FCM_EDGES.objects.filter(fcm_id=fcm.id)  # pairno edo oles tis akmes pou yparhoun pleon
                        j = 0
                        for i in c:  # edo kano update se kathe fcm_edge pou einai sti vasi ta parakato stoixeia
                            i.title = x2[j]['label']
                            i.from_node = x2[j]['from']
                            i.to_node = x2[j]['to']
                            j += 1
                            i.save()

                        messages.success(request, 'edited successfully')
                    else:
                        messages.error(request, "You must login to edit a map")
                else:
                    messages.error(request, "form invalid")
            data = {'title': fcm.title, 'description': fcm.description, 'country': fcm.country, 'status': fcm.status, 'chartis': fcm.chartis}
            form = jsForm(initial=data)
            form1 = chartisForm()
            #form.fields['chartis'].widget = forms.HiddenInput()
            #form.fields['map_image'].widget = forms.HiddenInput()
            #form.fields['map_html'].widget = forms.HiddenInput()

            return render(request, 'fcm_app/edit_fcm2.html', {
                'form': form,
                'fcm': fcm,
                'form1': form1,
            })
        return HttpResponseForbidden()


@login_required
def create_fcm(request):
    # s = render_to_string('fcm_app/remove_messages.html', {}, request)
    if request.method == 'POST':
        form = jsForm(request.POST)
        if form.is_valid():
            print(request)
            print(request.user)
            user = request.user
            if user.is_authenticated():
                fcm = FCM(user=user,
                          title=form.cleaned_data['title'],
                          description=form.cleaned_data['description'],
                          country = form.cleaned_data['country'],
                          chartis = form.cleaned_data['chartis'],
                          image_url=form.cleaned_data['image'],
                          creation_date=datetime.now(),
                          manual = True)
                fcm.save()
                tags = form.cleaned_data['tags']
                for tag_element in tags:
                    try:
                        new_tag = Tags(name=str(tag_element))
                        new_tag.save()
                    except DatabaseError:
                        pass
                    fcm.tags.add(str(tag_element))
                #searchTimi = request.POST.get('timi_pou_thelo', '')
                #searchTimi2 = request.POST.get('description', '')   # thelei to name, oxi to id
                #print("Some output")
                print(form.cleaned_data['chartis'])
                description_json = json.loads(form.cleaned_data['chartis'])
                #import pdb; pdb.set_trace()
                print(description_json)
                x = description_json
                x1 = x['nodes']  #list pou exei dictionaries
                x2 = x['edges']  #list
                #PROSOHI AN EINAI MIDEN

                for i in x1:
                    fcm_concept = FCM_CONCEPT(fcm=fcm, title = i['label'], id_in_fcm= i['id'], x_position = i['x'], y_position = i['y'])
                    fcm_concept.save()
                for i in x2:
                    fcm_edges = FCM_EDGES(fcm=fcm, title = i['label'], id_in_fcm_edges= i['id'], from_node = i['from'], to_node= i['to'])
                    fcm_edges.save()
                messages.success(request, 'Successfully created the System Map. <br> Add more info to the Map\'s Concepts <a href="/fcm/view-fcm-concept/' + str(fcm.id) + '/"><u>here</u></a>, or you can browse the rest of the maps <a href="/fcm/browse"><u>here</u></a>. ')
                #print(searchTimi)
                #print(searchTimi2)
                #print("Some output")
                #p1 = mynew(description=searchTimi)
                #p1.save()
                #p2 = mynew(description = form.cleaned_data['description'])
                #p2.save()
            else:
                messages.error(request, "You must login to create a FCM")
        else:
            messages.error(request, "form invalid")
        return redirect('/fcm/create_map')
    #data = {'title': "", 'description': "arxiko"}
    form = jsForm()

    return render(request, 'fcm_app/create_fcm.html', {
        'form': form,
    })