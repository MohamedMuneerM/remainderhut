
from django.views import generic
from .forms import RemainderForm
from .models import Remainder


class RemainderCreateView(generic.FormView):
	form_class = RemainderForm
	success_url = "."
	model = Remainder
	template_name = "remainder-create.html"

	def form_valid(self, form):
		form.save(user=self.request.user)
		return super().form_valid(form)

	



