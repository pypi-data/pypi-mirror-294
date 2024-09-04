from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentPreferences(models.TextChoices):
    NEWS = "NEWS", _("News")
    DEALS = "DEALS", _("Deals")
    TIPS = "TIPS", _("Tips")


class FrequencyPreferences(models.TextChoices):
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")


class LanguagePreferences(models.TextChoices):
    EN = "EN", _("English")
    ES = "FA", _("Spanish")
    FR = "AR", _("Arabic")
