from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.admin.views.decorators import staff_member_required

from gallery.views import ImageUploadAddView, ImageUploadListView, QuickActionView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'artgal.views.home', name='home'),
    # url(r'^artgal/', include('artgal.foo.urls')),
    url(r'^upload/$', ImageUploadAddView.as_view()),
    url(r'^list/$', ImageUploadListView.as_view()),
    url(r'^mod/(?P<action>\w+)/(?P<pk>\d+)/$', staff_member_required(QuickActionView.as_view())),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
