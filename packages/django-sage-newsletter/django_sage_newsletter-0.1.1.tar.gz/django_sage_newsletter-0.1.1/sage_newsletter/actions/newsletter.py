from django.utils.translation import gettext_lazy as _


class NewsletterSubscriptionActions:
    @staticmethod
    def confirm_subscriptions(modeladmin, request, queryset):
        queryset.update(confirmed=True)

    confirm_subscriptions.short_description = _("Confirm selected subscriptions")

    @staticmethod
    def deactivate_subscriptions(modeladmin, request, queryset):
        queryset.update(is_active=False)

    deactivate_subscriptions.short_description = _("Deactivate selected subscriptions")
