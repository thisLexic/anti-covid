from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import user_passes_test
from .forms import CommuterForm, EditCommuterForm, FindRouteForm
from .models import Commuters, Allowed_Routes
from .mixins import CommuterRequiredMixin
from cities.models import Cities
from transportations.models import Routes, Directions

def in_commuter_group(user):
    if user.is_authenticated:
        if user.groups.get().name == 'commuter':
            return Commuters.objects.filter(user_id=user).exists()
    return False

class CommuterUpdate(CommuterRequiredMixin, UpdateView):
    model = Commuters
    template_name = 'commuters/edit.html'
    form_class = EditCommuterForm
    context_object_name = 'commuter'
    success_url = reverse_lazy('commuters:view_my_routes')

    def form_valid(self, form):
        commuter = form.save(commit=False)
        commuter.updated_by = self.request.user
        commuter.updated_at = timezone.now()
        commuter.save()
        return redirect('commuters:view_my_routes')

    def get_object(self, *args, **kwargs):
        commuter = Commuters.objects.get(user_id=self.kwargs['pk'])
        if commuter.user_id != self.request.user:
            raise PermissionDenied()
        return commuter

def create_commuter(request):
    try:
        Commuters.objects.get(user_id=request.user)
        return HttpResponseRedirect(reverse('commuters:announcements'))
    except:
        pass
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.user.groups.get().name == "commuter":
        pass
    else:
        raise PermissionDenied
    if request.method == "POST":
        form = CommuterForm(request.POST)
        if form.is_valid():
            commuter = form.save(commit=False)
            commuter.user_id = request.user
            form.save()
            return redirect('commuters:view_my_routes')
    else:
        try:
            commuter = Commuters.objects.get(user_id=request.user.id)
            commuter_id = commuter.id
            return redirect('commuters:view_my_routes')
        except:
            form = CommuterForm
    return render(request, 'commuters/commuters_form.html', {
            'form':form,
        })

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def view_my_routes(request):
    commuter = Commuters.objects.get(user_id=request.user.id)
    routes_allowed = Allowed_Routes.objects.filter(commuter_id=commuter).select_related('route_id')
    routes_active = routes_allowed.filter(route_id__is_active=True)
    routes_inactive = routes_allowed.filter(route_id__is_active=False)
    allowed = routes_active.filter(status="A")
    pending = routes_active.filter(status="P")
    rejected = routes_active.filter(status="R")
    return render(request, 'routes/view_my_routes.html', {
            'commuter':commuter,
            'allowed':allowed,
            'pending':pending,
            'rejected':rejected,
            'routes_inactive':routes_inactive,
        })

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def find_route(request):
    if request.method == "POST":
        form = FindRouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            city = route.city_id
            routes = Routes.objects.filter(city_id=city, is_active=True)
            return render(request, 'routes/routes.html', {'routes':routes,
                'city':city})
    else:
        form = FindRouteForm
    return render(request, 'routes/apply_city.html', {
            'form':form,
        })

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def apply_route(request, pk):
    route = Routes.objects.get(id=pk)
    directions = Directions.objects.filter(route_id=route
        ).only('start_location', 'end_location'
        ).prefetch_related('times')
    try:
        allowed_route = Allowed_Routes.objects.get(
            commuter_id=Commuters.objects.get(user_id=request.user.id),
            route_id=route)
    except:
        allowed_route = False
    return render(request, 'routes/apply_route.html', {
            'directions':directions,
            'route':route,
            'allowed_route':allowed_route,
        })

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def apply_route_action(request, pk):
    try:
        allowed_route = Allowed_Routes(
            route_id=Routes.objects.get(id=pk),
            commuter_id=Commuters.objects.get(user_id=request.user),
            status='P')
        allowed_route.save()
    except:
        pass
    return redirect('commuters:view_my_routes')

# 
class AnnouncementsList(CommuterRequiredMixin, ListView):
    template_name = 'commuters/announcements.html'
    context_object_name = 'cities'

    def get_queryset(self):
        try:
            commuter = Commuters.objects.filter(user_id=self.request.user
                ).prefetch_related('allowed_routes__route_id__city_id'
                ).get()
        except:
            return Commuters.objects.none()
        cities = []
        for ar in commuter.allowed_routes.select_related('route_id__city_id').iterator():
            city = ar.route_id.city_id
            if city in cities:
                continue
            else:
                if city.major_is_active or city.minor_is_active:
                    cities.append(city)
        return cities


def load_lives_cities(request):
    province_id = request.GET.get('lives_province_id')
    cities = Cities.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

def load_works_cities(request):
    province_id = request.GET.get('works_province_id')
    cities = Cities.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = Cities.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})