from django import forms
from .models import Remainder


class RemainderForm(forms.ModelForm):
	when = forms.DateTimeField()
	class Meta:
		model = Remainder
		fields = "__all__"
		exclude = ("user",)
	