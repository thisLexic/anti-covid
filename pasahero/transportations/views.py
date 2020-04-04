from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Routes, Directions
from .forms import SubmitCommuterID, SubmitRouteID
from cities.models import Cities
from commuters.models import Commuters
from commuters.forms import FindRouteForm

def view_cities(request):
    if request.method == "POST":
        form = FindRouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            city = route.city_id
            routes = Routes.objects.filter(city_id=city, is_active=True)
            return render(request, 'anon/routes.html', {'routes':routes,
                'city':city})
    else:
        form = FindRouteForm
    return render(request, 'anon/see_city.html', {
            'form':form,
        })

def view_routes(request, pk):
    city = Cities.objects.filter(id=pk).prefetch_related('routes').get()
    routes = city.routes.only('id','name','is_active').filter(is_active=True)
    if not routes:
        message = "There are currently no Routes for this city"
    else:
        message = ""
    return render(request, 'view_routes.html', {
            'routes':routes,
            'city':city,
            'message':message,
        })

def view_directions(request, pk):
    directions = Directions.objects.filter(route_id__exact=pk
        ).defer('duration_minutes','vehicle'
        ).prefetch_related('times')
    try:
        route = directions[0].route_id
    except:
        route = "There are currently no trips for this route."
    return render(request, 'view_directions.html', {
            'data':directions,
            'route':route,
        })

def view_allowed_routes(request):
    message = ''

    if request.method == "POST":
        form = request.POST
        commuter_id = form['commuter_number']
        try:
            commuter = Commuters.objects.get(id=commuter_id)
            allowed_routes = commuter.allowed_routes.select_related('route_id')
            routes = []
            for ar in allowed_routes:
                routes.append(ar.route_id)
            return render(request, 'view_allowed_routes.html', {
                    'form':[],
                    'routes':routes,
                    'id':commuter_id,
                })
        except ObjectDoesNotExist:
            message = 'The Commuter Number '+ commuter_id +' does not exist. Kindly try again.'
    form_blank = SubmitCommuterID
    return render(request, 'view_allowed_routes.html', {
            'form':form_blank,
            'message':message
        })


def view_allowed_commuters(request):
    message = ''
    if request.method == "POST":
        form = request.POST
        route_id = form['route_number']
        try:
            route = Routes.objects.get(id=route_id)
            allowed_routes = route.allowed_routes.filter(status="A").select_related('commuter_id')
            commuters = []
            for ar in allowed_routes:
                commuters.append(ar.commuter_id)
            return render(request, 'view_allowed_commuters.html', {
                    'form':[],
                    'commuters':commuters,
                    'id':route_id,
                })
        except ObjectDoesNotExist:
            message = 'The Route Number '+ route_id +' does not exist. Kindly try again.'
    form_blank = SubmitRouteID
    return render(request, 'view_allowed_commuters.html', {
            'form':form_blank,
            'message':message
        })

def view_my_routes(request):
    def has_commuter_entry(user):
        try:
            commuter = Commuters.objects.get(user_id=user.id)
            return True
        except:
            pass
        return False

    if in_commuter_group(request.user):
        if has_commuter_entry(request.user):
            commuter = Commuters.objects.get(user_id=request.user.id)
            allowed_routes = commuter.allowed_routes.select_related('route_id')
            routes = []
            for ar in allowed_routes:
                routes.append(ar.route_id)
            return render(request, 'view_my_routes.html', {
                    'commuter':commuter,
                    'routes':routes
                })
        else:
            return HttpResponseRedirect(reverse('commuters:create_commuter'))
    else:
        message = "Invalid username or password. Please try again."
        return render(request, 'login.html', {'message':message})