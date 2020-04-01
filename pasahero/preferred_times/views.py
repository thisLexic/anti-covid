from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import user_passes_test
from .models import Preferred_Times
from .forms import CreateUpdatePreferredTimesForm
from commuters.views import in_commuter_group
from commuters.mixins import CommuterRequiredMixin
from commuters.models import Commuters, Allowed_Routes

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def view_allowed_routes(request):
    commuter = Commuters.objects.get(user_id=request.user.id)
    routes_allowed = Allowed_Routes.objects.filter(commuter_id=commuter).select_related('route_id')
    routes = routes_allowed.filter(route_id__is_active=True, status="A")
    return render(request, 'list_allowed_routes.html', {
            'routes':routes,
        })

class Create(CommuterRequiredMixin, CreateView):
    template_name = 'preferred_times.html'
    form_class = CreateUpdatePreferredTimesForm
    success_url = reverse_lazy('preferred_times:list')

    def get_context_data(self, **kwargs):
        allowed_route = Allowed_Routes.objects.filter(id=self.kwargs['pk']).select_related("commuter_id", 'route_id', 'preferred_time')
        commuter = Commuters.objects.get(user_id=self.request.user)
        allowed_route = allowed_route.get()
        if allowed_route.commuter_id != commuter:
            raise PermissionDenied()
        route = allowed_route.route_id
        ctx = super(Create, self).get_context_data(**kwargs)
        ctx['route'] = route
        return ctx

    def form_valid(self, form):
        preferred_time = form.save(commit=False)
        preferred_time.allowed_route_id = Allowed_Routes.objects.get(id=self.kwargs['pk'])
        preferred_time.save()
        return HttpResponseRedirect(reverse_lazy('preferred_times:list'))

class Update(CommuterRequiredMixin, UpdateView):
    template_name = 'preferred_times.html'
    form_class = CreateUpdatePreferredTimesForm
    success_url = reverse_lazy('preferred_times:list')

    def get_object(self, *args, **kwargs):
        allowed_route = Allowed_Routes.objects.filter(id=self.kwargs["pk"]).select_related('preferred_time')
        return allowed_route.get().preferred_time

    def get_context_data(self):
        allowed_route = Allowed_Routes.objects.filter(id=self.kwargs['pk']).select_related("commuter_id", 'route_id', 'preferred_time')
        commuter = Commuters.objects.get(user_id=self.request.user)
        allowed_route = allowed_route.get()
        if allowed_route.commuter_id != commuter:
            raise PermissionDenied()
        route = allowed_route.route_id
        ctx = super(Update, self).get_context_data()
        ctx['route'] = route
        return ctx

class UpdateCreateRedirectView(CommuterRequiredMixin, RedirectView):
   def get_redirect_url(self, pk):
        allowed_route = Allowed_Routes.objects.filter(id=pk).select_related('preferred_time')
        try:
            allowed_route.get().preferred_time
            return reverse('preferred_times:update', kwargs={'pk':pk})
        except:
            return reverse('preferred_times:create', kwargs={'pk':pk})