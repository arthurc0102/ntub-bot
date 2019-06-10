from django import forms


class FillForm(forms.Form):
    SCORE_CHOICES = (
        (5, '非常同意'),
        (4, '同意'),
        (3, '尚可'),
        (2, '不同意'),
        (1, '非常不同意'),
    )

    score = forms.ChoiceField(choices=SCORE_CHOICES, label='分數')
    suggestions = forms.CharField(required=False,
                                  widget=forms.Textarea(),
                                  label='建議事項（選填）')

    def clean(self):
        cleaned_data = super().clean()

        try:
            score = int(cleaned_data['score'])
        except Exception:
            raise forms.ValidationError('分數必須是數字')

        self.cleaned_data['score'] = score
