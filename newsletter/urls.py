from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import MailingDetailView

urlpatterns = [
    path("create/", views.CreateMailingView.as_view(), name="create_mailing"),
    path(
        "statistics/", views.UserMailingReportsView.as_view(), name="mailing_statistics"
    ),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path("recipient/", views.RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient/create/",
        views.RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipient/<int:pk>/update/",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete/",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailings/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "mailings/<int:mailing_id>/start/",
        views.MailingStartView.as_view(),
        name="mailing_start",
    ),
    path(
        "mailings/<int:mailing_id>/detail/",
        MailingDetailView.as_view(),
        name="mailing_detail",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
