from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django_tables2.export.export import TableExport
from django_tables2 import LazyPaginator, RequestConfig
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import PermissionRequiredMixin


class MyCreate:
    """This mixin has the methods to create a model."""

    is_create = False

    def create(self):
        self.is_create = True
        self.form_isvalid()
        messages.success(
            self.request,
            _("{} was created successfully").format(self.object)
        )


class MyFormValid:
    """
    This mixin has the method to check if form is valid and call the correct method.
    """

    reset_form = False

    def form_isvalid(self):
        form = self.get_form()
        if form.is_valid():
            self.custom_response = self.form_valid(form)
            self.reset_form = True
        else:
            self.custom_response = self.form_invalid(form)


class MyCreateMixin(MyCreate, MyFormValid):
    """This mixin has the methods create a model."""
    pass


class MyFilterSetTableMixin:
    filterset_class = None

    def get_filterset_class(self):
        """Return the filter class to use."""
        if self.filterset_class == None:
            klass = type(self).__name__
            raise ImproperlyConfigured(
                '{0} is missing the filterset_class attribute.'.format(klass)
            )

        return self.filterset_class

    def get_filterset(self):
        """Returns an instance of the filterset to be used in this view."""
        filterset_class = self.get_filterset_class()
        kwargs = self.get_filterset_kwargs()
        filterset = filterset_class(**kwargs)

        return filterset

    def get_filterset_kwargs(self):
        """Returns the keyword arguments for instantiating the filterset."""
        kwargs = {
            'data': self.get_GET_data() or None,
            'request': self.request,
        }

        return kwargs

    def get_filterset_queryset(self):
        """Return the filter queryset, it may be used as data to a table."""
        filterset = self.get_filterset()

        return filterset.qs


class MyTableMixin:
    table_class = None
    table_data = None
    context_table_name = "table"
    table_pagination_class = LazyPaginator
    per_page = 20
    export_table_name = "table"
    export_formats = ['csv', 'xls', 'xlsx']

    def get_context_table_name(self, table):
        """Get the name to use for the table's template variable."""
        return self.context_table_name

    def get_table_class(self):
        """Return the table class to use."""
        if self.table_class == None:
            klass = type(self).__name__
            raise ImproperlyConfigured(
                '{0} is missing the table_class attribute.'.format(klass)
            )
        return self.table_class

    def get_per_page(self):
        """
        Return the number of objects per page, if not passed by GET, return the default per_page.
        """
        if self.request.GET.get('per_page', None):
            return self.request.GET.get('per_page')
        return self.per_page

    def get_table_pagination(self, table):
        """Return a LazyPagination as default paginator."""
        paginate = {
            "per_page": self.get_per_page(),
            "paginator_class": self.table_pagination_class
        }

        return paginate

    def get_table(self, **kwargs):
        """Return an instance of the table to be used in this view."""
        table_class = self.get_table_class()
        table = table_class(data=self.get_table_data(), **kwargs)
        return RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)

    def get_table_data(self):
        """Return the table data that should be used to populate the rows."""
        if self.table_data is not None:
            return self.table_data
        elif hasattr(self, "get_filterset_queryset"):
            return self.get_filterset_queryset()

        klass = type(self).__name__
        raise ImproperlyConfigured(
            "Table data was not specified. Define {}.table_data".format(klass)
        )

    def get_table_kwargs(self):
        """
        Return the keyword arguments for instantiating the table.

        Allows passing customized arguments to the table constructor, for example,
        to remove the buttons column, you could define this method in your View::

            def get_table_kwargs(self):
                return {
                    'exclude': ('buttons', )
                }
        """
        return {}

    def get_export_table_response(self, export_format):
        """Export the data table with given format."""
        exporter = TableExport(export_format, self.get_table())
        return exporter.response("{}.{}".format(self.export_table_name, export_format))


class MyFormMixin:
    """Provide a way to show and handle a form in a request."""
    initial = {}
    form_class = None
    success_url = None
    form_prefix = None
    # Set to true to show a modal form, used when form has error or it
    # needs to be shown, like as an edit.
    show_modal = False

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_prefix(self):
        """Return the form_prefix to use for forms."""
        return self.form_prefix

    def get_form_class(self):
        """Return the form class to use."""
        return self.form_class

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        # If reset_form is true, so not pass data, files and neither instance
        if self.request.method in ('POST', 'PUT') and not self.reset_form:
            kwargs.update({
                'data': self.get_POST_data(),
                'files': self.request.FILES,
            })

        if not self.reset_form and self.get_object():
            kwargs.update({'instance': self.object})

        return kwargs

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        with transaction.atomic():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        self.show_modal = True
        return None
        # return self.render_to_response(self.get_context_data(form=form))


class MyExtraFormMixin:
    """
    Provide a way to handle a extra form in a request, this extra form is related with the form in MyFormMixin. It must be used along side the MyFormMixin class. This just add a new extra form and a way to valid and save it.
    """
    initial_extra = {}
    form_class_extra = None
    form_prefix_extra = None

    def get_initial_extra(self):
        """Return the initial data to use for forms on this view."""
        return self.initial_extra.copy()

    def get_prefix_extra(self):
        """Return the form_prefix to use for forms."""
        return self.form_prefix_extra

    def get_form_class_extra(self):
        """Return the form class to use."""
        return self.form_class_extra

    def get_form_extra(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class_extra()
        return form_class(**self.get_form_extra_kwargs())

    def get_object_extra(self):
        """
        It must be override.
        Return the object for extra form. Normally it is something like object.extra_object. For default it return None.       
        """
        return None

    def get_form_extra_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial_extra(),
            'prefix': self.get_prefix_extra(),
        }

        # If reset_form is true, so not pass data, files and neither instance.
        # The reset_form is from MyFormMixin but it works in the same way here.
        if self.request.method in ('POST', 'PUT') and not self.reset_form:
            kwargs.update({
                'data': self.get_POST_data(),
                'files': self.request.FILES,
            })

        # the instance is related to the main object
        extra_object = self.get_object_extra()
        if not self.reset_form and extra_object:
            kwargs.update({'instance': extra_object})

        return kwargs


class MyViewCreateMixin(LoginRequiredMixin, PermissionRequiredMixin, MyFormMixin, MyCreateMixin, MyFilterSetTableMixin, MyTableMixin, View):
    """This is a custom view mixin that offer view, and create a model."""

    model_class = None
    template_name = None
    page_title = None
    page_title_icon = None
    object = None
    extra_context = None
    # This is a custom response that will substitute the GET and POST
    # render response, normally only on update, delete and create will
    # change this field (always after doing some save form or delete
    # an object). If you wish to keep the GET data or some state that
    # is related to response, you can check on get and post methods
    # and comment the code that returns it.
    custom_response = None

    def get_context_data(self):
        """Return the context data, also check for fields."""
        if self.template_name == None:
            raise ImproperlyConfigured(
                '{0} is missing the template_name attribute.'.format(
                    self.__class__.__name__)
            )

        context = {
            'page_title': self.page_title,
            'page_title_icon': self.page_title_icon,
            'form': self.get_form(),
            'filter': self.get_filterset(),
            'table': self.get_table(),
            'export_formats': self.export_formats,
            'show_modal': self.show_modal,
            'object': self.get_object(),
        }

        extra_context = self.get_extra_context()
        if extra_context:
            context.update(extra_context)

        return context

    def get_extra_context(self):
        """Return the extra context data, override to pass yours."""
        return self.extra_context

    def get_GET_data(self):
        """
        Return the copy of GET data, sometimes it is needed to change the data from a request, but the data from a request is imutable (for security reasons), the copy of the data is not imutable.

        Override this method to process the GET data as you wish.
        """
        return self.request.GET.copy()

    def get_POST_data(self):
        """
        Same as get_GET_data but with the POST data.

        Override this method to process the POST data as you wish. Here the default processing is just send the copy of the POST data.
        """
        return self.request.POST.copy()

    def get_object(self):
        """Return an object, it must be override to return the right object."""
        return self.object

    def get(self, request, *args, **kwargs):
        # check if user request a export table if so then export
        export_format = request.GET.get("_export", None)
        if TableExport.is_valid_format(export_format):
            return self.get_export_table_response(export_format)
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # if the id is different from 0, it is an update
        self.create()
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())
