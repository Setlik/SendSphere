from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('create/', views.CreateMailingView.as_view(), name='create_mailing'),
    path('statistics/', views.MailingStatisticsView.as_view(), name='mailing_statistics'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('mailing/<pk>/start/', views.MailingStartView.as_view(), name='mailing_start'),

    path('clients/', views.RecipientListView.as_view(), name='recipient_list'),
    path('clients/create/', views.RecipientCreateView.as_view(), name='recipient_create'),
    path('clients/<int:pk>/update/', views.RecipientUpdateView.as_view(), name='recipient_update'),
    path('clients/<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),

    path('mailings/<int:pk>/send/', views.send_mailing, name='send_mailing'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)