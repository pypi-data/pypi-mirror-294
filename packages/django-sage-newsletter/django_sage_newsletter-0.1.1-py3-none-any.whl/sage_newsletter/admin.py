from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .actions import NewsletterSubscriptionActions
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Newsletter Subscriber Admin."""

    save_on_top = True
    list_display = (
        "email",
        "date_subscribed",
        "confirmed",
        "preferences",
        "frequency",
        "language",
        "is_active",
    )
    list_filter = (
        "confirmed",
        "preferences",
        "frequency",
        "language",
        "is_active",
        "gdpr_consent",
    )
    search_fields = ("email",)
    readonly_fields = ("date_subscribed", "unsubscribe_token", "last_sent")
    fieldsets = (
        (
            _("Subscriber Information"),
            {"fields": ("email", "date_subscribed", "confirmed")},
        ),
        (_("Preferences"), {"fields": ("preferences", "frequency", "language")}),
        (
            _("Subscription Status"),
            {"fields": ("is_active", "gdpr_consent", "unsubscribe_token", "last_sent")},
        ),
    )
    actions = [
        NewsletterSubscriptionActions.confirm_subscriptions,
        NewsletterSubscriptionActions.deactivate_subscriptions,
    ]
