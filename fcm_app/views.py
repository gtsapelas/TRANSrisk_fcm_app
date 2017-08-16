from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'a_var': "no_value"}
    return render(request, 'fcm_app/index.html', context)


def browse(request):
    context = {'a_var': "no_value"}
    return render(request, 'fcm_app/browse.html', context)
