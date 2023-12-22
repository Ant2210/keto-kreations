from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """ A custom clearable file input widget for the product image field """

    # Override the default clear checkbox label
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    # Override the template_name attribute to use our template
    template_name = (
        'products/custom_widget_templates/'
        'custom_clearable_file_input.html'
        )
