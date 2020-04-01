from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

class EmployeeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.groups.get().name == 'employee':
                return super().dispatch(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(reverse('cities:login'))