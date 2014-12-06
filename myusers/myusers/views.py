from django.views.generic import TemplateView, DetailView, ListView, FormView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser

class HomepageView(TemplateView):
	template_name = "index.html"

class MyUserListView(ListView):
	model = MyUser
	def get_queryset(self):
		return self.model.objects.all()

class MyUserDetailView(DetailView):
	model = MyUser

class MyUserCreateView(FormView):
	template_name = 'myusers/myuser_create.html'
	form_class = MyUserCreationForm
	model = MyUser

	def form_valid(self, form):
		form.save()

		return super(MyUserCreateView, self).form_valid(form)

	def get_success_url(self):
		"""
		redirect to list
		"""
		return reverse_lazy('list')

class MyUserUpdateView(UpdateView):
	model = MyUser
	template_name = 'myusers/myuser_update.html'
	form_class = MyUserChangeForm

class MyUserDeleteView(DeleteView):
	model = MyUser
	success_url = reverse_lazy('list')