from django import forms
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.html import escape


class BootstrapErrorClass(ErrorList):

    def __str__(self):

        if not self:
            return ''

        return mark_safe('<div class="alert alert-danger">{}</div>'.format(
            ''.join(['<div class="error">%s</div>' % escape(e) for e in self])
        ))


class BootstrapMixin(object):

    # Don't apply `form-control` to these fields
    UNCONTROLLED_FIELDS = (
        forms.widgets.RadioSelect,
        forms.widgets.CheckboxInput,
        forms.widgets.FileInput
    )

    def __init__(self):

        for field_name in self.fields.keys():

            widget = self.fields[field_name].widget

            self.fields[field_name].label_suffix = ""
            if not isinstance(widget, self.UNCONTROLLED_FIELDS):
                widget.attrs.update({"class": "form-control"})


class BootstrappedForm(BootstrapMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(
            self, error_class=BootstrapErrorClass, *args, **kwargs)
        BootstrapMixin.__init__(self)
