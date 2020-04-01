from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from .models import Documents
from .forms import CreateDocumentForm, UpdateDocumentForm
from commuters.models import Commuters
from commuters.views import in_commuter_group
from commuters.mixins import CommuterRequiredMixin
from documents.models import Documents

@user_passes_test(in_commuter_group, login_url='/commuters/submit/')
def read(request):
    commuter = Commuters.objects.get(user_id=request.user)
    documents = commuter.documents.only('title', 'id')
    return render(request, 'read.html', {"documents":documents})

class CreateDocument(CommuterRequiredMixin, CreateView):
    model = Documents
    template_name = 'create.html'
    form_class = CreateDocumentForm
    success_url = reverse_lazy('documents:read')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.commuter_id = Commuters.objects.get(user_id=self.request.user.id)
        self.object.save()
        return super(CreateDocument, self).form_valid(form)

class DetailDocument(CommuterRequiredMixin, DetailView):
    model = Documents
    template_name = 'detail.html'
    context_object_name = 'document'

    def get_object(self, *args, **kwargs):
        obj = super(DetailDocument, self).get_object(*args, **kwargs)
        commuter = obj.commuter_id
        user_id = commuter.user_id
        if user_id != self.request.user:
            raise PermissionDenied()
        return obj

class UpdateDocument(CommuterRequiredMixin, UpdateView):
    form_class = UpdateDocumentForm
    template_name = 'edit_document.html'
    success_url = reverse_lazy('documents:read')

    def get_object(self):
        commuter = Commuters.objects.get(user_id=self.request.user)
        document = Documents.objects.filter(id=self.kwargs['pk']).select_related('commuter_id').get()
        if commuter == document.commuter_id:
            return document
        else:
            raise PermissionDenied

class DeleteDocument(CommuterRequiredMixin, DeleteView):
    template_name = "documents_confirm_delete.html"
    success_url = reverse_lazy("documents:read")
    context_object_name = 'document'
    def get_object(self):
        document = Documents.objects.get(id=self.kwargs['pk'])
        if document.commuter_id.user_id == self.request.user:
            return document
        raise PermissionDenied