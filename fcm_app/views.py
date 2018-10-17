from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import jsForm, FCMForm, FCMCONCEPTForm, FiltersForm, SortMapsForm, FCMEDGEForm
from .models import FCM
from .models import FCM_CONCEPT
from .models import FCM_CONCEPT_INFO
from .models import FCM_EDGES_IN_FCM_CONCEPT
from .models import FCM_EDGE_INFO
from . models import Tags
from django.contrib import messages
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from django import forms
import json, pdb
import urllib.parse as urllib
# import urllib2

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
    if request.method == 'GET':
        if 'hasFilters' in request.GET:
            if bool(request.GET['hasFilters']) is True:
                pass
            else:
                request.method = 'GET'
        else:
            request.method = 'POST'
    else:
        request.session['filter-post'] = request.POST

    if request.method == 'POST':
        filter_form = FiltersForm(request.session['filter-post'])
        if filter_form.is_valid():
            filtered_title_and_or_description = filter_form.cleaned_data['filtered_title_and_or_description']
            filtered_year = filter_form.cleaned_data['filtered_year']
            filtered_country = filter_form.cleaned_data['filtered_country']
            filtered_getmine = filter_form.cleaned_data['filtered_getmine']
            filtered_tags = filter_form.cleaned_data['filtered_tags']
            filtered_sorting_type = filter_form.cleaned_data['filtered_sorting_type']
            filtered_sorting_order = filter_form.cleaned_data['filtered_sorting_order']


            if request.user.is_authenticated:
                all_fcms = FCM.objects.filter(Q(status='1') | Q(user=request.user)).order_by('-creation_date')
            else:
                all_fcms = FCM.objects.filter(Q(status='1')).order_by('-creation_date')
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

            if filtered_sorting_type == 'creation_date':
                if filtered_sorting_order == 'ASC':
                    all_fcms = all_fcms.order_by('creation_date')
                else:
                    all_fcms = all_fcms.order_by('-creation_date')
            elif filtered_sorting_type == 'title':
                if filtered_sorting_order == 'ASC':
                    all_fcms = all_fcms.order_by('title')
                else:
                    all_fcms = all_fcms.order_by('-title')

            data = {'filtered_title_and_or_description': filtered_title_and_or_description,
                    'filtered_year': filtered_year,
                    'filtered_country': filtered_country,
                    'filtered_getmine': filtered_getmine,
                    'filtered_tags': filtered_tags,
                    'filtered_sorting_type': filtered_sorting_type,
                    'filtered_sorting_order': filtered_sorting_order}
            filter_form = FiltersForm(initial=data)
            paginator = Paginator(all_fcms, 9)
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
        else:
            all_fcms = FCM.objects.filter(Q(status='1') | Q(user=request.user)).order_by('-creation_date')
            return render(request, 'fcm_app/browse.html', {"all_fcms": all_fcms, "filter_form": filter_form})
    else:

        #all_fcms = FCM.objects.all()
        if request.user.is_authenticated:
            all_fcms = FCM.objects.filter(Q(status='1') | Q(user=request.user)).order_by('-creation_date')
        else:
            all_fcms = FCM.objects.filter(Q(status='1')).order_by('-creation_date')
        filter_form = FiltersForm()
        paginator = Paginator(all_fcms, 9)
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
            try:
                print(request.user)
                user = request.user
                soup = BeautifulSoup(form.cleaned_data['map_html'], "html.parser")  # vazo i lxml  i html.parser
                if len(soup.find("table", class_="yimagetable")) > 0:
                    print("src in html: " + soup.find("img", class_="yimage")['src'])
                    print("image name: " + form.cleaned_data['map_image'].name)
                    if urllib.unquote(soup.find("img", class_="yimage")['src']) == form.cleaned_data['map_image'].name:
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
                                if str(div['id']).startswith("n"):
                                    fcm_concept = FCM_CONCEPT(fcm=fcm, title=div.text, id_in_fcm=div.get('id'))
                                    fcm_concept.save()
                                else:
                                    fcm_edge = FCM_EDGES_IN_FCM_CONCEPT(fcm=fcm, text=div.text, id_in_fcm=div.get('id'))
                                    fcm_edge.save()
                            messages.success(request, 'Successfully imported the System Map. Add more info <a style="color: #a05017;" href="/fcm/view-fcm-concept/' + str(fcm.id) + '/"><u>here</u></a>, or you can browse the rest of the Maps <a  style="color: #a05017;" href="/fcm/browse?hasFilters=false"><u>here</u></a>. ')
                        else:
                            messages.error(request, "You must login to import a map")
                    else:
                        messages.error(request, "The image you uploaded does not match with the html file")
                else:
                    messages.error(request, "The html file was not exported from yEd")
            except:
                messages.error(request, "Import failed, please check the files you uploaed")
        else:
            messages.error(request, "form invalid")
    form = FCMForm()
    return render(request, 'fcm_app/import_fcm.html', {
        'form': form
    })


def view_fcm(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    # fcm.chartis = str(fcm.chartis)

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
                info_dict[str(concepts_item.id_in_fcm)] = 'No more information available'

        edges = FCM_EDGES_IN_FCM_CONCEPT.objects.filter(fcm=fcm)
        print(edges)
        for edge_item in edges:
            try:
                edge_info = FCM_EDGE_INFO.objects.get(fcm_edge=edge_item)
                info_dict[str(edge_item.id_in_fcm)] = edge_info.info
            except FCM_EDGE_INFO.DoesNotExist:
                info_dict[str(edge_item.id_in_fcm)] = 'No more information available'
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
                info_dict[str(concepts_item.id_in_fcm)] = 'No more information available'
        print(info_dict)

        edges = FCM_EDGES_IN_FCM_CONCEPT.objects.filter(fcm=fcm)
        print('edges:')
        # print(edges)
        info_edge_dict = dict()
        for edge_item in edges:
            try:
                edge_info = FCM_EDGE_INFO.objects.get(fcm_edge=edge_item)
                info_edge_dict[str(edge_item.id_in_fcm)] = edge_info.info
            except FCM_EDGE_INFO.DoesNotExist:
                info_edge_dict[str(edge_item.id_in_fcm)] = 'No more information available'
        print(info_edge_dict)

        return render(request, 'fcm_app/view_fcm4.html', {
            'fcm': fcm,
            #'data1': x,
            #'form': form,
            'info_dict': info_dict,
            'info_edge_dict': info_edge_dict,
        })


@login_required
def delete_fcm(request, fcm_id):
    FCM.objects.get(pk=fcm_id).delete()
    return render(request, 'fcm_app/index.html', {})


@login_required
def view_fcm_concept(request, fcm_id):
    fcm = FCM.objects.get(pk=fcm_id)
    if request.user == fcm.user:
        concepts = FCM_CONCEPT.objects.filter(fcm=fcm_id)
        relations = FCM_EDGES_IN_FCM_CONCEPT.objects.filter(fcm=fcm_id)
        return render(request, 'fcm_app/view_fcm_concept.html', {"fcm_id": fcm_id, "concepts": concepts, "relations": relations})
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
def view_fcm_edge_info(request, fcm_id, edge_id):
    storage = messages.get_messages(request)
    storage.used = True
    fcm = FCM.objects.get(pk=fcm_id)
    if request.user == fcm.user:
        edge = FCM_EDGES_IN_FCM_CONCEPT.objects.get(fcm=fcm_id, pk=edge_id)
        edge_info = FCM_EDGE_INFO()
        try:
            edge_info = FCM_EDGE_INFO.objects.get(fcm_edge=edge_id)
            data = {'edge_info': edge_info.info}
        except edge_info.DoesNotExist:
            data = {}

        form = FCMEDGEForm(initial=data)
        if request.method == 'POST':
            form = FCMEDGEForm(request.POST)
            if form.is_valid():
                my_edge = get_object_or_404(FCM_EDGES_IN_FCM_CONCEPT, pk=edge_id)
                fcm_edge_info = FCM_EDGE_INFO()
                try:
                    fcm_edge_info = FCM_EDGE_INFO.objects.get(fcm_edge=my_edge)
                    fcm_edge_info.info = form.cleaned_data['edge_info']
                except fcm_edge_info.DoesNotExist:
                    fcm_edge_info = FCM_EDGE_INFO(fcm_edge=my_edge, info=form.cleaned_data['edge_info'])
                fcm_edge_info.save()
                messages.success(request, 'edited successfully')
            else:
                messages.error(request, "an error occured")
        return render(request, 'fcm_app/view_fcm_edge_info.html/', {
            'form': form, 'relation': edge,
        })
    return HttpResponseForbidden()

@login_required
def my_fcms(request):

    if request.method == 'POST':
        sort_maps_form = SortMapsForm(request.POST)
        if sort_maps_form.is_valid():
            my_fcms = []
            user = request.user
            if user.is_authenticated():
                my_fcms = FCM.objects.filter(user=user)
                sorting_type = sort_maps_form.cleaned_data['sorting_type']
                if sorting_type == 'creation_date':
                    my_fcms = my_fcms.order_by('-creation_date')
                else:
                    my_fcms = my_fcms.order_by('title')

                return render(request, 'fcm_app/my_fcms.html/', {
                    'my_fcms': my_fcms,
                    "sort_maps_form": sort_maps_form
                })

    sort_maps_form = SortMapsForm()
    my_fcms = []
    user = request.user
    if user.is_authenticated():
        my_fcms = FCM.objects.filter(user=user)
    return render(request, 'fcm_app/my_fcms.html/', {
        'my_fcms': my_fcms,
        "sort_maps_form": sort_maps_form
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

                        for tag_element in fcm.tags.all():
                            tag_element.delete()

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
            tags = [t.name for t in fcm.tags.all()]
            data = {'title': fcm.title, 'description': fcm.description, 'country': fcm.country, 'status': fcm.status}
            print(tags)
            form = FCMForm(initial=data)
            # pdb.set_trace()
            form.fields['map_image'].widget = forms.HiddenInput()
            form.fields['map_html'].widget = forms.HiddenInput()

            return render(request, 'fcm_app/edit_fcm.html', {
                'form': form,
                'fcm': fcm,
                'tags': tags
            })
        return HttpResponseForbidden()
    else:
        if request.user == fcm.user:
            if request.method == 'POST':
                #data = {'map_image': fcm.map_image, 'map_html': fcm.map_html}
                #data = {'chartis': fcm.chartis}
                #print(data)
                form = jsForm(request.POST)
                # pdb.set_trace()
                if form.is_valid():
                    print(request.user)
                    user = request.user
                    if user.is_authenticated():
                        fcm.title=form.cleaned_data['title']
                        fcm.description=form.cleaned_data['description']
                        fcm.country=form.cleaned_data['country']
                        fcm.status=form.cleaned_data['status']
                        fcm.chartis = form.cleaned_data['chartis']
                        fcm.image_url = form.cleaned_data['image']
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

                        description_json = json.loads(form.cleaned_data['chartis'])

                        print(description_json)
                        x = description_json
                        x1 = x['nodes']  # list pou exei dictionaries
                        x2 = x['edges']  # list

                        for concept in FCM_CONCEPT.objects.filter(fcm=fcm):
                            concept.delete()

                        for edge in FCM_EDGES_IN_FCM_CONCEPT.objects.filter(fcm=fcm):
                            edge.delete()

                        for i in x1:
                            fcm_concept = FCM_CONCEPT(fcm=fcm, title=i['label'], id_in_fcm=i['id'], x_position=i['x'], y_position=i['y'])
                            fcm_concept.save()
                            if str(i['concept_info']).strip() != "":
                                fcm_concept_info = FCM_CONCEPT_INFO(fcm_concept=fcm_concept, info=str(i['concept_info']).strip())
                                fcm_concept_info.save()
                        for i in x2:
                            fcm_edges_in_fcm_concept = FCM_EDGES_IN_FCM_CONCEPT(fcm=fcm, id_in_fcm=i['id'], text=i['label'], from_concept=
                            FCM_CONCEPT.objects.filter(fcm=fcm).filter(id_in_fcm=i['from'])[0], to_concept=
                                                                                FCM_CONCEPT.objects.filter(fcm=fcm).filter(id_in_fcm=i['to'])[0])
                            fcm_edges_in_fcm_concept.save()
                            if str(i['relation_info']).strip() != "":
                                fcm_relation_info = FCM_EDGE_INFO(fcm_edge=fcm_edges_in_fcm_concept, info=str(i['relation_info']).strip())
                                fcm_relation_info.save()

                        messages.success(request, 'edited successfully')
                    else:
                        messages.error(request, "You must login to edit a map")
                else:
                    messages.error(request, "form invalid")
            data = {'title': fcm.title, 'description': fcm.description, 'country': fcm.country, 'status': fcm.status, 'chartis': fcm.chartis}
            form = jsForm(initial=data)

            tags = [t.name for t in fcm.tags.all()]
            print(tags)

            #form.fields['chartis'].widget = forms.HiddenInput()
            #form.fields['map_image'].widget = forms.HiddenInput()
            #form.fields['map_html'].widget = forms.HiddenInput()

            concept_info_form = FCMCONCEPTForm()
            relation_info_form = FCMEDGEForm()

            return render(request, 'fcm_app/edit_fcm2.html', {
                'form': form,
                'fcm': fcm,
                'tags': tags,
                'concept_info_form': concept_info_form,
                'relation_info_form': relation_info_form
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
                    if str(i['concept_info']).strip() != "":
                        fcm_concept_info = FCM_CONCEPT_INFO(fcm_concept=fcm_concept, info=str(i['concept_info']).strip())
                        fcm_concept_info.save()
                for i in x2:
                    fcm_edges_in_fcm_concept = FCM_EDGES_IN_FCM_CONCEPT(fcm=fcm, id_in_fcm= i['id'], text=i['label'], from_concept=FCM_CONCEPT.objects.filter(fcm=fcm).filter(id_in_fcm=i['from'])[0], to_concept=FCM_CONCEPT.objects.filter(fcm=fcm).filter(id_in_fcm=i['to'])[0])
                    fcm_edges_in_fcm_concept.save()
                    if str(i['relation_info']).strip() != "":
                        fcm_relation_info = FCM_EDGE_INFO(fcm_edge=fcm_edges_in_fcm_concept, info=str(i['relation_info']).strip())
                        fcm_relation_info.save()

                messages.success(request, 'Successfully created the System Map. <br> Add more info to the Map\'s Concepts and Relations <a style="color: #a05017;"  href="/fcm/view-fcm-concept/' + str(fcm.id) + '/"><u>here</u></a>, or you can browse the rest of the maps <a  style="color: #a05017;" href="/fcm/browse?hasFilters=false"><u>here</u></a>. ')
            else:
                messages.error(request, "You must login to create a map")
        else:
            messages.error(request, "form invalid")
        return redirect('/fcm/create_map')
    form = jsForm()
    concept_info_form = FCMCONCEPTForm()
    relation_info_form = FCMEDGEForm()
    return render(request, 'fcm_app/create_fcm.html', {
        'form': form,
        'concept_info_form': concept_info_form,
        'relation_info_form': relation_info_form
    })
