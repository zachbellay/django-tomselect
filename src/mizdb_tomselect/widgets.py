import json

from django import forms
from django.urls import reverse


class MIZSelect(forms.Select):
    """
    A TomSelect widget with model object choices.

    The TomSelect element will be configured using custom data attributes on
    the select element, which are provided by the widget's `build_attrs` method.
    """

    def __init__(
        self,
        model,
        url="autocomplete",
        search_lookup="name__icontains",
        value_field="id",
        label_field="name",
        create_field="",
        multiple=False,
        changelist_url="",
        add_url="",
        filter_by=(),
        **kwargs,
    ):
        """
        Instantiate a MIZSelect widget.

        Args:
            model: the django model that the choices are derived from
            url: the URL pattern name of the view that serves the choices and
              handles requests from the TomSelect element
            search_lookup: a Django field lookup to use with the given search
              term to filter the results
            value_field: the name of the model field that corresponds to the
              choice value of an option (f.ex. 'id')
            label_field: the name of the model field that corresponds to the
              human-readable value of an option (f.ex. 'name')
            create_field: the name of the model field used to create new
              model objects with
            multiple: if True, allow selecting multiple options
            changelist_url: URL name of the changelist view for this model
            add_url: URL name of the add view for this model
            filter_by: a 2-tuple (form_field_name, field_lookup) to filter the
              results against the value of the form field using the given
              Django field lookup. For example:
               ('foo', 'bar__id') => results.filter(bar__id=data['foo'])
            kwargs: additional keyword arguments passed to forms.Select
        """
        self.model = model
        self.url = url
        self.search_lookup = search_lookup
        self.create_field = create_field
        self.value_field = value_field
        self.label_field = label_field
        self.multiple = multiple
        self.changelist_url = changelist_url
        self.add_url = add_url
        self.filter_by = filter_by
        super().__init__(**kwargs)

    def optgroups(self, name, value, attrs=None):
        return []  # Never provide any options; let the view serve the options.

    def get_url(self):
        """Hook to specify the autocomplete URL."""
        return reverse(self.url)

    def get_add_url(self):
        """Hook to specify the URL to the model's add page."""
        if self.add_url:
            return reverse(self.add_url)

    def get_changelist_url(self):
        """Hook to specify the URL the model's changelist."""
        if self.changelist_url:
            return reverse(self.changelist_url)

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        opts = self.model._meta
        attrs.update(
            {
                "is-tomselect": True,
                "is-multiple": self.multiple,
                "data-autocomplete-url": self.get_url(),
                "data-model": f"{opts.app_label}.{opts.model_name}",
                "data-search-lookup": self.search_lookup,
                "data-value-field": self.value_field,
                "data-label-field": self.label_field,
                "data-create-field": self.create_field,
                "data-changelist-url": self.get_changelist_url() or "",
                "data-add-url": self.get_add_url() or "",
                "data-filter-by": json.dumps(list(self.filter_by)),
            }
        )
        return attrs

    class Media:
        css = {
            "all": ["vendor/tom-select/css/tom-select.bootstrap5.css", "mizdb_tomselect/css/mizselect.css"],
        }
        js = ["mizdb_tomselect/js/mizselect.js"]


class MIZSelectTabular(MIZSelect):
    """A MIZSelect widget that displays results in a table with a table header."""

    def __init__(self, *args, extra_columns=None, value_field_label="ID", label_field_label="Object", **kwargs):
        """
        Instantiate a MIZSelectTabular widget.

        Args:
            extra_columns: a mapping of <model field names> to <column labels>
              for additional columns. The field name tells TomSelect what
              values to look up on a model object result for a given column.
              The label is the table header label for a given column.
            value_field_label: table header label for the value field column
            label_field_label: table header label for the label field column
            args: additional positional arguments passed to MIZSelect
            kwargs: additional keyword arguments passed to MIZSelect
        """
        super().__init__(*args, **kwargs)
        self.value_field_label = value_field_label
        self.label_field_label = label_field_label
        self.extra_columns = extra_columns or {}

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update(
            {
                "is-tabular": True,
                "data-value-field-label": self.value_field_label,
                "data-label-field-label": self.label_field_label,
                "data-extra-headers": json.dumps(list(self.extra_columns.values())),
                "data-extra-columns": json.dumps(list(self.extra_columns.keys())),
            }
        )
        return attrs
