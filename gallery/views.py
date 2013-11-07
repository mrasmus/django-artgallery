from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
import json
from gallery.models import ImageUpload, Gallery

class ImageUploadAddView(CreateView):
    model = ImageUpload
    success_url = '/'

    def get_initial(self):
        initial = super(ImageUploadAddView, self).get_initial()
        initial = initial.copy()
        initial['gallery'] = Gallery.objects.all()[0]
        initial['approved'] = True
        return initial

    def get_form(self, form_class):
        form = super(ImageUploadAddView, self).get_form(form_class)
        form.fields['gallery'].empty_label = "Select a Gallery..."
        if self.request.user and self.request.user.is_staff:
            pass
        else:
            form.fields.pop('approved')
        return form


class ImageUploadListView(ListView):
    model = Gallery


class QuickActionView(View):
    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            action = kwargs.get('action')
            if action not in ['approve','unapprove','delete']:
                raise
            img = ImageUpload.objects.get(pk=pk)
            if action == 'delete':
                img.delete()
            else:
                img.approved = (action == 'approve')
                img.save()
            response_data = {'status': 'SUCCESS'}
        except:
            response_data = {'status': 'FAILURE'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")