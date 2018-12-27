from django import forms


class ConfirmForm(forms.Form):
    check_label = '你確定要執行這個動作嗎？'
    check = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check'].label = self.check_label
