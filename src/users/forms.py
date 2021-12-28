from django import forms
from .models import Remainder


class RemainderForm(forms.ModelForm):
	class Meta:
		model = Remainder
		fields = "__all__"
		exclude = ("user",)

	def __init__(self, *args, **kwargs):
		super(RemainderForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	