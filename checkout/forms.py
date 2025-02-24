from django import forms
from django.utils.html import format_html, mark_safe
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.translation import gettext as _


class UserInfo(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    

class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        hidden_fields = "".join(str(field) for field in self.hidden_fields())  # Properly render hidden inputs
        return format_html(
            """<form action="{0}" method="post">
                {1}
                <div class="d-grid gap-2 my-3">
                    <button class="btn btn-primary" type="submit">
                        <i class="lni lni-paypal-original"></i> {2}
                    </button>
                </div>
            </form>""",
            self.get_login_url(),
            mark_safe(hidden_fields),  # Ensure it is treated as safe HTML
            _('Pay Now')
        )
