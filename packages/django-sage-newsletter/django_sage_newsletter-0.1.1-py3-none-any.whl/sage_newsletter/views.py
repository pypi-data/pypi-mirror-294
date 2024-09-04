from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin

from .forms import NewsletterSubscriptionForm


class NewsletterViewMixin(ContextMixin):
    """A mixin to add newsletter subscription functionality to a view.

    This mixin provides functionalities for handling the newsletter
    subscription form. It can be mixed into any Django view to add these
    capabilities.

    """

    form_class = NewsletterSubscriptionForm
    form_context_object = "newsletter_form"
    success_url_name = None

    def __init__(self, *args, **kwargs):
        """Initialize the view.

        Raises:
            ImproperlyConfigured: If success_url_name is not set in the subclass.

        """
        super().__init__(*args, **kwargs)
        if not self.success_url_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'success_url_name' attribute. "
                "You must define 'success_url_name' in your view."
            )

    def get_context_data(self, **kwargs):
        """Inserts the form into the context dict for rendering.

        This method extends the base `get_context_data` method to add the newsletter
        subscription form to the context, making it available in the template.

        Args:
            **kwargs: Keyword arguments from the view.

        Returns:
            dict: The context dictionary with the form included.

        """
        context = super().get_context_data(**kwargs)
        context[self.form_context_object] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """Handles POST requests for newsletter subscription.

        This method processes the newsletter subscription form. If the form is valid,
        it either adds a new subscription or reactivates an existing one. Appropriate
        success messages are displayed to the user after processing.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects to the specified URL on success.
            HttpResponse: Renders the template with context on failure.

        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if hasattr(form, "reactivated") and form.reactivated:
                messages.success(
                    request,
                    _(
                        "We've reactivated your email address. Thanks for subscribing again!"
                    ),
                )
            else:
                messages.success(
                    request, _("You have successfully subscribed to the newsletter.")
                )
            return redirect(request.path)

        # Check if the view has a get_queryset method
        if hasattr(self, "get_queryset"):
            self.object_list = self.get_queryset()

        # Handling for DetailView
        if isinstance(self, DetailView):
            self.object = self.get_object()

        context = self.get_context_data()
        context[self.form_context_object] = form
        return render(request, self.template_name, context)
