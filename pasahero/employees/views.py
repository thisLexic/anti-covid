import io
import datetime
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import FileResponse
from django.db.models.functions import Lower
from .models import Employees
from .mixins import EmployeeRequiredMixin
from .forms import CreateRouteForm, CreateDirectionForm, CreateTimeFormSet
from commuters.models import Commuters, Allowed_Routes
from transportations.models import Routes, Directions, Times
from documents.models import Documents
from reportlab.pdfgen import canvas
from urllib.parse import urlencode

def in_employee_group(user):
    try:
        if user.groups.get().name == 'employee':
            return True
    except:
        pass
    return False

@user_passes_test(in_employee_group, login_url='/manage/login')
def home_page(request):
    city = Employees.objects.get(user_id=request.user).city_id
    return render(request, 'emp_home_page.html', {
            'city':city,
        })

@user_passes_test(in_employee_group, login_url='/manage/login')
def announcements(request):
    city = Employees.objects.get(user_id=request.user).city_id
    if city.major_is_active and city.minor_is_active:
        status = "maj_min"
    elif city.major_is_active and not city.minor_is_active:
        status = "maj"
    elif not city.major_is_active and city.minor_is_active:
        status = "min"
    else:
        status = "none"
    return render(request, 'announcements.html', {
            'city':city,
            'status':status,
        })

class ListActiveRoutes(EmployeeRequiredMixin, ListView):
    template_name = 'active_routes.html'
    context_object_name = 'routes'

    def get_queryset(self, *args, **kwargs):
        routes = Routes.objects.filter(
                        is_active=True,
                        city_id=Employees.objects.get(user_id=self.request.user
                            ).city_id
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

class ListInactiveRoutes(EmployeeRequiredMixin, ListView):
    template_name = 'inactive_routes.html'
    context_object_name = 'routes'
    
    def get_queryset(self, *args, **kwargs):
        routes = Routes.objects.filter(
                        is_active=False,
                        city_id=Employees.objects.get(user_id=self.request.user
                            ).city_id
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


class RouteDetail(EmployeeRequiredMixin, DetailView):
    template_name = 'detail_view.html'
    context_object_name = 'route'

    def get_object(self):
        pk = self.kwargs['pk']
        emp_city = Employees.objects.get(user_id=self.request.user).city_id
        route = Routes.objects.filter(id=pk
            ).select_related('city_id',
                'employee_id'
            ).prefetch_related('directions__times',
            ).get()
        if route.city_id == emp_city:
            return route
        else:
            raise PermissionDenied

class CommutersList(EmployeeRequiredMixin, ListView):
    template_name = 'commuters_list.html'
    context_object_name = 'allowed_routes'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        route = Routes.objects.get(id=pk)
        if route.city_id == Employees.objects.get(user_id=self.request.user
            ).city_id:
            status = self.kwargs['status']
            status = status.upper()
            allowed_routes = Allowed_Routes.objects.filter(
                    status=status,
                    route_id=route,
                ).select_related('commuter_id',
                    'commuter_id__works_city_id',
                    'commuter_id__lives_city_id',
                ).order_by('requested_at',
                    'commuter_id__works_city_id__name',
                    'commuter_id__lives_city_id__name',)

            page = self.request.GET.get('page', 1)
            paginator = Paginator(allowed_routes, 10)
            try:
                allowed_routes = paginator.page(page)
            except PageNotAnInteger:
                allowed_routes = paginator.page(1)
            except EmptyPage:
                allowed_routes = paginator.page(paginator.num_pages)

            return {'allowed_routes':allowed_routes,
                    'route':route
                }
        else:
            raise PermissionDenied

class CommuterDetail(EmployeeRequiredMixin, DetailView):
    template_name = 'commuter_detail.html'
    context_object_name = 'commuter'

    def get_object(self):
        pass

    def get_context_data(self, **kwargs):
        commuter = Commuters.objects.get(id=self.kwargs['pk'])
        employee = Employees.objects.select_related("city_id").get(user_id=self.request.user)
        city = employee.city_id

        allowed = Allowed_Routes.objects.filter(
            commuter_id=commuter,
            route_id__city_id=city,
        )
        if allowed:
            allowed_route = Allowed_Routes.objects.select_related('route_id',
                ).get(id=self.kwargs['pk_ar'])
            route = allowed_route.route_id
            return {'commuter':commuter,
                'allowed_route':allowed_route,
                'route':route
            }
        else:
            raise PermissionDenied

@user_passes_test(in_employee_group, login_url='/manage/login')
def decision_commuter(request, pk_ar, pk_route, old_status, new_status):
    allowed_route = Allowed_Routes.objects.select_related('route_id__city_id').get(id=pk_ar)
    route = Routes.objects.get(id=pk_route)
    city = allowed_route.route_id.city_id
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    if city == emp_city:
        allowed_route.status = new_status
        allowed_route.employee_id = employee
        allowed_route.save()
        return HttpResponseRedirect(reverse('employees:commuters_list', kwargs={
                'pk':route.id,
                'status':old_status,
            }))

        kwargs={'app_label': 'auth'}
    else:
        raise PermissionDenied

class DocumentDetail(EmployeeRequiredMixin, DetailView):
    template_name = 'document_detail.html'
    context_object_name = 'document'

    def get_object(self):
        pass

    def get_context_data(self, **kwargs):
        document = Documents.objects.get(id=self.kwargs['doc_pk'])
        employee = Employees.objects.get(user_id=self.request.user)
        route = Routes.objects.get(id=self.kwargs['route_pk'])
        if route.city_id == employee.city_id:
            return {'document':document}
        else:
            raise PermissionDenied

class CreateRoute(EmployeeRequiredMixin, CreateView):
    model = Routes
    template_name = 'add_route.html'
    form_class = CreateRouteForm
    success_url = reverse_lazy('employees:active')

    def form_valid(self, form):
        employee = Employees.objects.select_related('city_id',
            'city_id__province_id'
            ).get(user_id=self.request.user)
        city = employee.city_id
        province = city.province_id
        self.object = form.save(commit=False)
        self.object.is_active = True
        self.object.city_id = city
        self.object.province_id = province
        self.object.employee_id = employee
        self.object.save()
        return super(CreateRoute, self).form_valid(form)

@user_passes_test(in_employee_group, login_url='/manage/login')
def change_status_route(request, pk):
    route = Routes.objects.get(id=pk)
    city = route.city_id
    employee = Employees.objects.get(user_id=request.user)
    if city == employee.city_id:
        route.employee_id = employee
        route.is_active = not route.is_active
        route.save()
        if route.is_active:
            return HttpResponseRedirect(reverse_lazy('employees:inactive'))
        return HttpResponseRedirect(reverse_lazy('employees:active'))
    else:
        raise PermissionDenied

@user_passes_test(in_employee_group, login_url='/manage/login')
def add_directions(request, pk):
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    route = Routes.objects.get(id=pk)
    city = route.city_id
    if city == emp_city:
        if request.method == 'GET':
            form_direction = CreateDirectionForm
        elif request.method == "POST":
            form_direction = CreateDirectionForm(request.POST)
            direction = form_direction.save(commit=False)
            direction.route_id = route
            direction.save()
            route = direction.route_id
            route.employee_id = employee
            route.save()
            return HttpResponseRedirect(reverse('employees:details_route',
                    kwargs={
                    'pk':route.id,
                }))
        return render(request, 'create_directions.html',{
            'form_direction':form_direction,
            'route_id':pk,
        })
    else:
        raise PermissionDenied

@user_passes_test(in_employee_group, login_url='/manage/login')
def edit_directions(request, route_pk, dir_pk):
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    route = Routes.objects.get(id=route_pk)
    city = route.city_id
    if city == emp_city:
        if request.method == 'GET':
            direction = Directions.objects.get(id=dir_pk)
            form_direction = CreateDirectionForm(instance=direction)
        elif request.method == "POST":
            form_direction = CreateDirectionForm(request.POST)
            new_direction = form_direction.save(commit=False)
            old_direction = Directions.objects.get(id=dir_pk)
            old_direction.start_location = new_direction.start_location
            old_direction.end_location = new_direction.end_location
            old_direction.vehicle = new_direction.vehicle
            old_direction.duration_minutes = new_direction.duration_minutes
            old_direction.save()
            route = old_direction.route_id
            route.employee_id = employee
            route.save()
            return HttpResponseRedirect(reverse('employees:details_route',
                    kwargs={
                    'pk':route.id,
                }))
        return render(request, 'edit_directions.html',{
            'form_direction':form_direction,
            'route_pk':route_pk,
            'dir_pk':dir_pk,
        })
    else:
        raise PermissionDenied

@user_passes_test(in_employee_group, login_url='/manage/login')
def add_times(request, dir_pk):
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    direction = Directions.objects.select_related('route_id__city_id').get(id=dir_pk)
    city = direction.route_id.city_id
    if city != emp_city:
        raise PermissionDenied
    if request.method == "POST":
        formset = CreateTimeFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    try:
                        time = form.save(commit=False)
                        time.direction_id = direction
                        time.save()
                    except:
                        break
                    route = time.direction_id.route_id
                    route.employee_id = employee
                    route.save()
        return HttpResponseRedirect(reverse('employees:details_route',
            kwargs={"pk":direction.route_id.id}))
    else:
        formset = CreateTimeFormSet
    return render(request, 'add_times.html',
        {
            'form':formset,
            'dir_pk':dir_pk
        })

@user_passes_test(in_employee_group, login_url='/manage/login')
def delete_direction(request, route_pk, dir_pk):
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    route = Routes.objects.get(id=route_pk)
    city = route.city_id
    if city != emp_city:
        raise PermissionDenied
    else:
        direction = Directions.objects.filter(id=dir_pk).delete()
        route.employee_id = employee
        route.save()
    return HttpResponseRedirect(reverse('employees:details_route',
            kwargs={
            'pk':route.id,
        }))


class TimesList(EmployeeRequiredMixin, ListView):
    template_name = 'times_list.html'
    context_object_name = 'times'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        dir_pk = self.kwargs['dir_pk']
        direction = Directions.objects.select_related("route_id__city_id"
            ).prefetch_related('times'
            ).get(id=dir_pk)
        route = direction.route_id
        if route.city_id == Employees.objects.get(user_id=self.request.user
            ).city_id:
            times = direction.times.all()
            return {'times':times,
                    'dir_pk':dir_pk
                }
        else:
            raise PermissionDenied

@user_passes_test(in_employee_group, login_url='/manage/login')
def time_delete(request, dir_pk, t_pk):
    employee = Employees.objects.get(user_id=request.user)
    emp_city = employee.city_id
    direction = Directions.objects.select_related('route_id__city_id').get(id=dir_pk)
    city = direction.route_id.city_id
    if city != emp_city:
        raise PermissionDenied
    else:
        time = Times.objects.filter(id=t_pk)
        route = time.get().direction_id.route_id
        route.employee_id = employee
        route.save()
        time.delete()
    return HttpResponseRedirect(reverse('employees:list_times',
            kwargs={
            'dir_pk':dir_pk,
        }))

@user_passes_test(in_employee_group, login_url='/manage/login')
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
    return render(request, 'change_password.html', {
        'form': form
    })

@user_passes_test(in_employee_group, login_url='/manage/login')
def pdf(request, pk, status):
    route = Routes.objects.filter(id=pk).prefetch_related('allowed_routes').get()
    status = status.upper()
    allowed_routes = route.allowed_routes.filter(status=status
        ).select_related('commuter_id'
        ).order_by(Lower("commuter_id__last_name"))
    if status == "A":
        title = "Approved Commuters"
    elif status == "P":
        title = "Pending Commuters"
    elif status == "R":
        title = 'Rejected Commuters'
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    size =740
    p.drawString(20, 800, datetime.datetime.now().strftime("%Y-%m-%d"))
    p.drawString(20, 790, route.name)
    p.drawString(20, 780, title)

    p.drawString(20, 760, "First Name")
    p.drawString(270, 760, "Last Name")

    for allowed_route in allowed_routes:
        commuter = allowed_route.commuter_id
        if size < 20:
            size = 740
            p.showPage()

            p.drawString(20, 800, datetime.datetime.now().strftime("%Y-%m-%d"))
            p.drawString(20, 790, route.name)
            p.drawString(20, 780, title)

            p.drawString(20, 760, "First Name")
            p.drawString(270, 760, "Last Name")
        p.drawString(20, size+10, "---------------------------------------------------------------------------------------------------------------------------------")
        p.drawString(20, size, commuter.first_name)
        p.drawString(270, size, commuter.last_name)
        size -= 20
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=title+".pdf")

@user_passes_test(in_employee_group, login_url='/manage/login')
def employee_preferred_time(request, pk, flip):
    employee = Employees.objects.get(user_id=request.user)
    route = Routes.objects.filter(id=pk).prefetch_related("allowed_routes").get()
    if route.city_id != employee.city_id:
        raise PermissionDenied
    allowed_routes = route.allowed_routes.filter(preferred_time__isnull=False).select_related('preferred_time')
    count = {"mon_a_to_b":{},
        "tues_a_to_b":{},
        "wed_a_to_b":{},
        "thurs_a_to_b":{},
        "fri_a_to_b":{},
        "sat_a_to_b":{},
        "sun_a_to_b":{},
        "mon_b_to_a":{},
        "tues_b_to_a":{},
        "wed_b_to_a":{},
        "thurs_b_to_a":{},
        "fri_b_to_a":{},
        "sat_b_to_a":{},
        "sun_b_to_a":{},
    }

    for ar in allowed_routes.iterator():
        try:
            count['mon_a_to_b'][ar.preferred_time.mon_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['mon_a_to_b'][ar.preferred_time.mon_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['tues_a_to_b'][ar.preferred_time.tues_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['tues_a_to_b'][ar.preferred_time.tues_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['wed_a_to_b'][ar.preferred_time.wed_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['wed_a_to_b'][ar.preferred_time.wed_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['thurs_a_to_b'][ar.preferred_time.thurs_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['thurs_a_to_b'][ar.preferred_time.thurs_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['fri_a_to_b'][ar.preferred_time.fri_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['fri_a_to_b'][ar.preferred_time.fri_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['sat_a_to_b'][ar.preferred_time.sat_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['sat_a_to_b'][ar.preferred_time.sat_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['sun_a_to_b'][ar.preferred_time.sun_a_to_b.strftime("%H%M")] += 1
        except KeyError:
            count['sun_a_to_b'][ar.preferred_time.sun_a_to_b.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['mon_b_to_a'][ar.preferred_time.mon_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['mon_b_to_a'][ar.preferred_time.mon_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['tues_b_to_a'][ar.preferred_time.tues_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['tues_b_to_a'][ar.preferred_time.tues_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['wed_b_to_a'][ar.preferred_time.wed_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['wed_b_to_a'][ar.preferred_time.wed_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['thurs_b_to_a'][ar.preferred_time.thurs_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['thurs_b_to_a'][ar.preferred_time.thurs_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['fri_b_to_a'][ar.preferred_time.fri_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['fri_b_to_a'][ar.preferred_time.fri_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['sat_b_to_a'][ar.preferred_time.sat_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['sat_b_to_a'][ar.preferred_time.sat_b_to_a.strftime("%H%M")] = 1
        except:
            pass
        try:
            count['sun_b_to_a'][ar.preferred_time.sun_b_to_a.strftime("%H%M")] += 1
        except KeyError:
            count['sun_b_to_a'][ar.preferred_time.sun_b_to_a.strftime("%H%M")] = 1
        except:
            pass
    return render(request, "preferred_time_emp.html", {
            "route":route,
            "count":count,
            'flip':flip,
        })