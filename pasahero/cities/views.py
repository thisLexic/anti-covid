from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .mixins import CityRequiredMixin
from .models import Cities
from .forms import CreateEmployeeForm, CreateUserForm, UpdateAnnouncementForm
from employees.models import Employees
from transportations.models import Routes

def in_cities_group(user):
    try:
        if user.groups.get().name == 'city':
            return True
    except:
        pass
    return False

@user_passes_test(in_cities_group, login_url='/manage/login')
def home(request):
    city = Cities.objects.get(user_id=request.user)
    if city.major_is_active and city.minor_is_active:
        status = "maj_min"
    elif city.major_is_active and not city.minor_is_active:
        status = "maj"
    elif not city.major_is_active and city.minor_is_active:
        status = "min"
    else:
        status = "none"
    return render(request, 'home_city.html', {
            'city':city,
            'status':status,
        })

class EmployeesList(CityRequiredMixin, ListView):
    template_name = 'emp_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        pass

    def get_context_data(self):
        employees = Employees.objects.filter(
            city_id=Cities.objects.get(user_id=self.request.user))
        employees_active = employees.filter(is_active=True)
        employees_inactive = employees.filter(is_active=False)
        return {'employees_active':employees_active,
            'employees_inactive':employees_inactive
        }

def login_city(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                if user.groups.get().name == "city":
                    login(request, user)
                    return HttpResponseRedirect(reverse('cities:home_page'))
                elif user.groups.get().name == "employee":
                    if Employees.objects.get(user_id=user).is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('employees:home_page'))
            except:
                pass
        message = "Invalid username or password. Please try again."
    return render(request, 'login_city.html', {'message':message})

class EmployeeDetail(CityRequiredMixin, DetailView):
    model = Employees
    template_name = 'employee_details.html'
    context_object_name = 'employee'

    def get_object(self, *args, **kwargs):
        try:
            obj = super(EmployeeDetail, self).get_object(*args, **kwargs)
            city = obj.city_id
            user_id = city.user_id
            if user_id == self.request.user:
                return obj
        except:
            pass
        return None

@user_passes_test(in_cities_group, login_url='/manage/login')
def create_employee(request):
    if request.method == "POST":
        user_form = CreateUserForm(data=request.POST)
        employee_form = CreateEmployeeForm(data=request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            employee_group = Group.objects.get(name='employee')
            employee_group.user_set.add(user)
            user.save()

            employee = employee_form.save(commit=False)
            employee.user_id = user
            employee.city_id = Cities.objects.get(user_id=request.user)
            employee.save()
            return HttpResponseRedirect(reverse('cities:home_page'))
    else:
        user_form = CreateUserForm()
        employee_form = CreateEmployeeForm()
    return render(request, 'employee_create.html',{
            'user_form':user_form,
            'employee_form':employee_form,
        })

class RoutesList(CityRequiredMixin, ListView):
    template_name = "routes_list.html"
    context_object_name = 'routes'

    def get_queryset(self):
        routes = Routes.objects.filter(
                        is_active=True,
                        city_id=Cities.objects.get(user_id=self.request.user
                            )
                    ).prefetch_related(
                        'allowed_routes'
                    )
        routes = routes.annotate(
            allowed=Count('allowed_routes', 
                filter=Q(allowed_routes__status="A"
                )
            ),
            pending=Count('allowed_routes', 
                filter=Q(allowed_routes__status="P"
                )
            ),
            rejected=Count('allowed_routes', 
                filter=Q(allowed_routes__status="R"
                )
            ),
        )
        return routes

@user_passes_test(in_cities_group, login_url='/manage/login')
def delete_route(request, pk):
    city = Cities.objects.get(user_id=request.user)
    route = Routes.objects.select_related('city_id').get(id=pk)
    if city == route.city_id:
        route.delete()
        return HttpResponseRedirect(reverse("cities:list_routes"))
    else:
        raise PermissionDenied

class UpdateAnnouncement(CityRequiredMixin, UpdateView):
    form_class = UpdateAnnouncementForm
    template_name = 'edit_announcement.html'
    success_url = reverse_lazy('cities:home_page')

    def get_object(self):
        return Cities.objects.get(user_id=self.request.user)

@user_passes_test(in_cities_group, login_url='/manage/login')
def employee_change(request, pk):
    employee = Employees.objects.get(id=pk)
    status = employee.is_active
    employee.is_active = not status
    employee.save()
    return HttpResponseRedirect(reverse("cities:employees_list"))

@user_passes_test(in_cities_group, login_url='/manage/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('employees:home_page')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password_cities.html', {
        'form': form
    })