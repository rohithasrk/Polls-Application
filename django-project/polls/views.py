from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question, Choice, UserProfile
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .forms import UserForm, UserProfileForm

#from django.template import loader

class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_question_list'

	def get_queryset(self):
		#return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	#if question.was_published_recently():
	model = Question
	template_name = 'polls/detail.html'
	#else:
	#	raise Http404

class ResultsView(generic.DetailView):
	model=Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html',{'question':question, 'error_message':"You didn't select a choice."})
	else:
		selected_choice.votes=+1
		selected_choice.save()
	
		return HttpResponseRedirect(reverse('polls:results',args=(question_id)))

def register(request):
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
	
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
		
			profile = profile_form.save(commit=False)
			profile.user=user
	
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				profile.save()
				registered=True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	return render(request, 'polls/register.html',{'user_form':user_form, 'profile_form':profile_form,'registered':registered})
