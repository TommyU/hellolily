from django.conf.urls import patterns, url

from lily.contacts.views import AddContactView, EditContactView, \
    DeleteContactView, EditFunctionView, ListContactView

urlpatterns = patterns('',
     url(r'^add/$', AddContactView.as_view(), name='contact_add'),
     url(r'^functions/(?P<pk>[\w-]+)/$', EditFunctionView.as_view(), name='function_edit'),
     url(r'^edit/(?P<pk>[\w-]+)/$', EditContactView.as_view(), name='contact_edit'),
     url(r'^delete/xhr/(?P<pk>[\w-]+)/$', DeleteContactView.as_view(), name='contact_delete'),
     url(r'^$', ListContactView.as_view(), name='contact_list'),
)