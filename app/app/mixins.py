from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http.response import Http404
from django_tables2.export.export import TableExport
from django_tables2 import LazyPaginator, RequestConfig
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.forms import modelformset_factory


class MyDelete:
    """This mixin has the methods to delete a model."""

    is_delete = False

    def get_selection(self):
        """Return the selection pks from POST."""
        return self.request.GET.getlist("selection", [])

    def get_selected_objects(self):
        """Return the selected objects in view or None."""
        selection = self.get_selection()
        if len(selection) > 0:
            return self.model_class.objects.filter(pk__in=selection)
        return None

    def delete(self):
        """Delete the selected models."""
        if self.check_delete_permission():
            selected_objects = self.get_selected_objects()
            count_objects = selected_objects.count()
            if selected_objects:
                selected_objects.delete()
            self.is_delete = True
            messages.success(
                self.request,
                _("{} objects deleted successfully").format(count_objects)
            )
            self.custom_response = HttpResponseRedirect(self.get_success_url())


class MyUpdate:
    """This mixin has the methods to update a model."""

    is_update = False

    def update(self):
        if self.check_edit_permission():
            self.is_update = True
            self.form_isvalid()
            messages.success(
                self.request,
                _("{} was edited successfully").format(self.object)
            )


class MyCreate:
    """This mixin has the methods to create a model."""

    is_create = False

    def create(self):
        if self.check_add_permission():
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


class MyCreateUpdateDeleteMixin(MyDelete, MyUpdate, MyCreate, MyFormValid):
    """This mixin has the methods to create, update and delete a model."""
    pass


class MyUpdateMixin(MyUpdate, MyFormValid):
    """This mixin has the methods update a model."""
    pass


class MyPermissionMixin:
    """Permission mixin to handle the permissions of a user to an object."""

    def get_permissions(self):
        """
        Get all the permissions that the user has of a given model.
        If user is super user the return will have all permissions.

        The permissions available are ['view', 'add', 'change', 'delete']
        """
        if self.request == None:
            raise ImproperlyConfigured(
                '{0} is missing the request attribute.'.format(
                    self.__class__.__name__)
            )

        # if is a super user return all the permissions
        if self.request.user.is_superuser:
            return ['view', 'add', 'change', 'delete']

        if self.model_class == None:
            raise ImproperlyConfigured(
                '{0} is missing the model_class attribute.'.format(
                    self.__class__.__name__)
            )

        permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(self.model_class),
            user=self.request.user
        )
        return [perm.codename.split('_')[0] for perm in permissions]

    def check_view_permission(self):
        """Check for permission to view"""
        if not any('view' in item for item in self.get_permissions()):
            raise PermissionDenied()
        return True

    def check_add_permission(self):
        """Check for permission to add"""
        if not any('add' in item for item in self.get_permissions()):
            raise PermissionDenied()
        return True

    def check_edit_permission(self):
        """Check for permission to change"""
        if not any('change' in item for item in self.get_permissions()):
            raise PermissionDenied()
        return True

    def check_delete_permission(self):
        """Check for permission to delete"""
        if not any('delete' in item for item in self.get_permissions()):
            raise PermissionDenied()
        return True


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


class MyFormSetMixin:
    """Mixin that provides a way to handle one formset."""
    formset_initial = {}
    formset_model_class = None
    formset_prefix = None
    # This a part of django_crispy forms
    formset_helper = None
    formset_queryset = None
    formset_can_delete = True

    def get_formset_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.formset_initial.copy()

    def get_formset_helper(self):
        """Return the formset helper, used in template."""
        return self.formset_helper

    def get_formset_prefix(self):
        """Return the form_prefix to use for forms."""
        return self.formset_prefix

    def get_formset_extra(self):
        """
        Return the amount of formset. Return 0 if queryset not empty and 1 if it is.
        """
        queryset = self.get_formset_queryset()
        if queryset and queryset.count() > 0:
            return 0
        return 1

    def get_formset_widgets(self):
        """Return a dict with widgets for formset."""
        return {}

    def get_formset_can_delete(self):
        """Return if can delete formset items. Default is True."""
        return self.formset_can_delete

    def get_formset_fields(self):
        """Return the fields of formset. Default is '__all__'."""
        return '__all__'

    def get_formset_factory(self):
        """Return the form class to use."""
        if not self.formset_model_class:
            klass = type(self).__name__
            raise ImproperlyConfigured(
                '{0} is missing formset_model_class attribute.'.format(klass)
            )

        return modelformset_factory(
            self.formset_model_class,
            fields=self.get_formset_fields(),
            extra=self.get_formset_extra(),
            can_delete=self.get_formset_can_delete(),
            widgets=self.get_formset_widgets()
        )

    def get_formset_queryset(self):
        """Return the queryset for the formset."""
        if not self.formset_model_class:
            klass = type(self).__name__
            raise ImproperlyConfigured(
                '{0} is missing formset_model_class attribute.'.format(klass)
            )

        return self.formset_model_class.objects.none()

    def get_formset_data(self):
        """Return formset data if is a POST or PUT."""
        if self.request.method in ('POST', 'PUT') and not self.reset_form:
            return self.get_POST_data()
        return None

    def get_formset_files(self):
        """Return formset files if is a POST or PUT."""
        if self.request.method in ('POST', 'PUT') and not self.reset_form:
            return self.request.FILES
        return None

    def get_formset(self):
        """Return an instance of the form to be used in this view."""

        formset_factory = self.get_formset_factory()
        formset = formset_factory(
            queryset=self.get_formset_queryset(),
            prefix=self.get_formset_prefix(),
            data=self.get_formset_data(),
            files=self.get_formset_files(),
        )
        return formset


class MyViewCreateUpdateDeleteMixin(LoginRequiredMixin, MyPermissionMixin, MyFilterSetTableMixin, MyTableMixin, MyFormMixin, MyCreateUpdateDeleteMixin, View):
    """
    This is a custom view mixin that offer view, add, edit and delete a model.

    It provides a table from django_tables2, a filterset from django_filterset and a form to edit and add new objects.
    """

    model_class = None
    template_name = None
    page_title = None
    page_title_icon = None
    object = None
    extra_context = {}
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
            'object': self.object,
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

        Override this method to process the GET data as you wish, the default processing is to check the reset-filter, if True reset the filter data (returning None).

        This view only has GET data because of the filter, so it is ok to do this things, but if you have others things that is sent by GET (for example the size of the table) you MUST find a way yo keep those data.
        """
        if self.request.GET.get('reset-filter', False):
            return None
        return self.request.GET.copy()

    def get_POST_data(self):
        """
        Same as get_GET_data but with the POST data.

        Override this method to process the POST data as you wish. Here the default processing is just send the copy of the POST data.
        """
        return self.request.POST.copy()

    def actions_trigger(self):
        """Trigger the right action, it could be delete or edit."""
        action = self.request.GET.get('actions')
        if action == 'delete':
            self.delete()
        elif action == 'edit':
            self.is_update = True
            if self.get_object():
                self.show_modal = True

    def get_object(self):
        """
        Return an object, first check if it has id on POST, then check if it has a selection on GET and get the first one. 

        Only return if is not is_delete, because if True the object no longer exists.
        """
        if self.model_class == None:
            raise ImproperlyConfigured(
                '{0} is missing the model_class attribute.'.format(
                    self.__class__.__name__)
            )
        if not self.object:
            if self.request.POST.get(self.form_prefix+"-id", "0") != "0":
                self.object = get_object_or_404(
                    self.model_class,
                    pk=self.request.POST.get(self.form_prefix+"-id")
                )
            elif self.request.GET.get('selection', None):
                self.object = get_object_or_404(
                    self.model_class,
                    pk=self.get_selection()[0]
                )
        return self.object

    def get(self, request, *args, **kwargs):
        if self.check_view_permission():
            # check if user request a export table if so then export
            export_format = request.GET.get("_export", None)
            if TableExport.is_valid_format(export_format):
                return self.get_export_table_response(export_format)
            self.actions_trigger()
            if self.custom_response:
                return self.custom_response
            return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # if the id is different from 0, it is an update
        if request.POST.get(self.form_prefix+"-id", "0") != "0":
            self.update()
        else:
            self.create()
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())


class MyViewCreateUpdateDeleteExtraFormMixin(MyViewCreateUpdateDeleteMixin, MyExtraFormMixin):
    """This is a custom view mixin that provides a extra form handle."""

    def get_extra_context(self):
        extra_context = {
            'form_extra': self.get_form_extra()
        }
        return extra_context

    def form_isvalid(self):
        with transaction.atomic():
            form = self.get_form()
            if form.is_valid():
                self.custom_response = self.form_valid(form)
                form_extra = self.get_form_extra()
                if form_extra.is_valid():
                    extra_object = form_extra.save(commit=False)
                    extra_object.product = self.object
                    extra_object.save()
                    self.reset_form = True
                else:
                    self.custom_response = self.form_invalid(form_extra)
            else:
                self.custom_response = self.form_invalid(form)


class MyViewCreateUpdateDeleteFormSetMixin(MyViewCreateUpdateDeleteMixin, MyFormSetMixin):
    """This is a custom view mixin that provides a formset handle."""

    def get_action_view(self):
        """
        Return the action view that is been performed. The default is create.
        """
        if self.is_update:
            return "edit"
        return "create"

    def get_extra_context(self):
        """Return the extra context."""
        self.extra_context.update({
            'formset': self.get_formset(),
            'formset_helper': self.get_formset_helper(),
            'action_view': self.get_action_view(),
        })
        return self.extra_context


class MyViewUpdateMixin(LoginRequiredMixin, MyPermissionMixin, MyFormMixin, MyUpdateMixin, View):
    """This is a custom view mixin that offer view, and edit a model."""

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
        if self.check_view_permission():
            if self.custom_response:
                return self.custom_response
            return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # if the id is different from 0, it is an update
        if request.POST.get(self.form_prefix+"-id", "0") != "0":
            self.update()
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())


class MyViewDeleteMixin(LoginRequiredMixin, MyPermissionMixin, MyFilterSetTableMixin, MyTableMixin, MyDelete, View):
    """View to display a list of objects and allow to delete."""

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
            'filter': self.get_filterset(),
            'table': self.get_table(),
            'export_formats': self.export_formats,
        }

        extra_context = self.get_extra_context()
        if extra_context:
            context.update(extra_context)

        return context

    def get_extra_context(self):
        """Return the extra context data, override to pass yours."""
        return self.extra_context

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def get_GET_data(self):
        """
        Return the copy of GET data, sometimes it is needed to change the data from a request, but the data from a request is imutable (for security reasons), the copy of the data is not imutable.

        Override this method to process the GET data as you wish.
        """
        return self.request.GET.copy()

    def actions_trigger(self):
        """Trigger the right action, it could be delete or edit."""
        action = self.request.GET.get('actions')
        if action == 'delete':
            self.delete()

    def get(self, request, *args, **kwargs):
        if self.check_view_permission():
            # check if user request a export table if so then export
            export_format = request.GET.get("_export", None)
            if TableExport.is_valid_format(export_format):
                return self.get_export_table_response(export_format)
            self.actions_trigger()
            if self.custom_response:
                return self.custom_response
            return render(request, self.template_name, self.get_context_data())

    # def post(self, request, *args, **kwargs):
    #     # if the id is different from 0, it is an update
    #     if request.POST.get(self.form_prefix+"-id", "0") != "0":
    #         self.update()
    #     if self.custom_response:
    #         return self.custom_response
    #     return render(request, self.template_name, self.get_context_data())


class MyDetailsFormSetMixin(LoginRequiredMixin, MyPermissionMixin, MyFormMixin, MyFormSetMixin, MyUpdateMixin, View):
    """
    This is a mixin to show details of a object, it provides a form to edit the object and a delete.
    """

    model_class = None
    template_name = None
    page_title = None
    page_title_icon = None
    object = None
    extra_context = {}
    # This is a custom response that will substitute the GET and POST
    # render response, normally only on update, delete and create will
    # change this field (always after doing some save form or delete
    # an object). If you wish to keep the GET data or some state that
    # is related to response, you can check on get and post methods
    # and comment the code that returns it.
    custom_response = None
    success_delete_url = None
    pk = None

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
            'show_modal': self.show_modal,
            'object': self.get_object(),
        }

        extra_context = self.get_extra_context()
        if extra_context:
            context.update(extra_context)
        return context

    def get_action_view(self):
        """
        Return the action view that is been performed. The default is edit.
        """
        return "edit"

    def get_extra_context(self):
        """Return the extra context."""
        self.extra_context.update({
            'formset': self.get_formset(),
            'formset_helper': self.get_formset_helper(),
            'action_view': self.get_action_view(),
        })
        return self.extra_context

    def get_GET_data(self):
        """Return the copy of GET data."""
        return self.request.GET.copy()

    def get_POST_data(self):
        """Return a copy of POST data."""
        return self.request.POST.copy()

    def get_success_delete_url(self):
        """Return success delete url."""
        if self.success_delete_url == None:
            raise ImproperlyConfigured(
                '{0} is missing the success_delete_url attribute.'.format(
                    self.__class__.__name__)
            )
        return str(self.success_delete_url)

    def delete(self):
        """Delete the object and redirect to success_delete_url."""

        if self.check_delete_permission():
            object = self.get_object()
            object.delete()
            self.is_delete = True
            messages.success(
                self.request,
                _("Object deleted successfully")
            )
            self.custom_response = HttpResponseRedirect(
                self.get_success_delete_url()
            )

    def actions_trigger(self):
        """Trigger the right action, it could be delete or edit."""
        action = self.request.GET.get('actions')
        if action == 'delete':
            self.delete()
        elif action == 'edit':
            self.update()

    def get_object(self):
        """Return an object, based on the pk passed on GET."""
        if self.model_class == None:
            raise ImproperlyConfigured(
                '{0} is missing the model_class attribute.'.format(
                    self.__class__.__name__)
            )
        if not self.object:
            if self.pk:
                self.object = get_object_or_404(self.model_class, pk=self.pk)
            else:
                raise Http404()
        return self.object

    def get(self, request, pk, *args, **kwargs):
        if self.check_view_permission():
            self.pk = pk
            self.actions_trigger()
            if self.custom_response:
                return self.custom_response
            return render(request, self.template_name, self.get_context_data())

    def post(self, request, pk, *args, **kwargs):
        self.pk = pk
        self.update()
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())


class MyDetailsFormMixin(LoginRequiredMixin, MyPermissionMixin, MyFormMixin,  MyUpdateMixin, View):
    """This is a mixin view that handle details with edit and delete."""

    model_class = None
    template_name = None
    page_title = None
    page_title_icon = None
    object = None
    extra_context = {}
    # This is a custom response that will substitute the GET and POST
    # render response, normally only on update, delete and create will
    # change this field (always after doing some save form or delete
    # an object). If you wish to keep the GET data or some state that
    # is related to response, you can check on get and post methods
    # and comment the code that returns it.
    custom_response = None
    success_delete_url = None
    pk = None

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
            'show_modal': self.show_modal,
            'object': self.get_object(),
            'action_view': self.get_action_view(),
        }

        extra_context = self.get_extra_context()
        if extra_context:
            context.update(extra_context)
        return context

    def get_action_view(self):
        """
        Return the action view that is been performed. The default is edit.
        """
        return "edit"

    def get_extra_context(self):
        """Return the extra context."""
        return self.extra_context

    def get_GET_data(self):
        """Return the copy of GET data."""
        return self.request.GET.copy()

    def get_POST_data(self):
        """Return a copy of POST data."""
        return self.request.POST.copy()

    def get_success_delete_url(self):
        """Return success delete url."""
        if self.success_delete_url == None:
            raise ImproperlyConfigured(
                '{0} is missing the success_delete_url attribute.'.format(
                    self.__class__.__name__)
            )
        return str(self.success_delete_url)

    def delete(self):
        """Delete the object and redirect to success_delete_url."""

        if self.check_delete_permission():
            object = self.get_object()
            object.delete()
            self.is_delete = True
            messages.success(
                self.request,
                _("Object deleted successfully")
            )
            self.custom_response = HttpResponseRedirect(
                self.get_success_delete_url()
            )

    def actions_trigger(self):
        """Trigger the right action, it could be delete or edit."""
        action = self.request.GET.get('actions')
        if action == 'delete':
            self.delete()
        elif action == 'edit':
            self.update()

    def get_object(self):
        """Return an object, based on the pk passed on GET."""
        if self.model_class == None:
            raise ImproperlyConfigured(
                '{0} is missing the model_class attribute.'.format(
                    self.__class__.__name__)
            )
        if not self.object:
            if self.pk:
                self.object = get_object_or_404(self.model_class, pk=self.pk)
            else:
                raise Http404()
        return self.object

    def get(self, request, pk, *args, **kwargs):
        if self.check_view_permission():
            self.pk = pk
            self.actions_trigger()
            if self.custom_response:
                return self.custom_response
            return render(request, self.template_name, self.get_context_data())

    def post(self, request, pk, *args, **kwargs):
        self.pk = pk
        self.update()
        if self.custom_response:
            return self.custom_response
        return render(request, self.template_name, self.get_context_data())
