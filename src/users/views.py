from django.views import generic
from .forms import RemainderForm
from .models import Remainder


class RemainderCreateView(generic.FormView):
	form_class = RemainderForm
	success_url = "."
	model = Remainder
	template_name = "remainder-create.html"

	def form_valid(self, form):
		form = form.save(commit=False)
		form.user = self.request.user
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		print(form)
		return super().form_valid(form)

class RemainderListView(generic.ListView):
	model = Remainder
	template_name = "remainder-list.html"
	context_object_name = "remainders" 

