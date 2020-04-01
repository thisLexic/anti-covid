from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from commuters.models import Commuters

class CommuterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.groups.get().name == 'commuter':
                if Commuters.objects.filter(user_id=request.user).exists():
                    return super().dispatch(request, *args, **kwargs)
        except:
            pass
        return  HttpResponseRedirect(reverse('commuters:create_commuter'))