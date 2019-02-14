from django.shortcuts import render
from .models import Date
from accounts.models import UserProfile
from suspicious.models import Suspicious
from .forms import DateCreateForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django import forms
import datetime

@method_decorator(login_required, name='dispatch')
class DateCreateView(CreateView):
    template_name   = 'date/create.html'
    form_class      = DateCreateForm

    def form_valid(self, form):
        today       = datetime.date.today()
        next_year   = datetime.datetime(year=today.year+1, month=1, day=1)
        start_date          = form.instance.start_date
        closure_date        = form.instance.closure_date
        final_closure_date  = form.instance.final_closure_date
        if not closure_date.day > start_date.day or not closure_date.month >= start_date.month:
            form.add_error(
                'closure_date', forms.ValidationError("Closure Date must be greater than Start Date!")
                )
            return super().form_invalid(form)
        if not final_closure_date.day >= closure_date.day or not final_closure_date.month >= closure_date.month or not final_closure_date.hour >= closure_date.hour:
            form.add_error(
                'final_closure_date', forms.ValidationError("Final Closure Date and Time must be greater than or equal Closure Date and Time!")
                )
            return super().form_invalid(form)
        form.instance.academic_year = "%s-%s" %(today.strftime("%Y"), next_year.strftime("%Y")[-2:])
        messages.add_message(self.request, messages.SUCCESS, 
            "New Schedule has been created successfully !"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('system_data:date_create')

    def user_passes_test(self, request):
        user = self.request.user
        user_profile_filter = UserProfile.objects.filter(user=user)
        if user_profile_filter.exists():
            user_profile = user_profile_filter.first()
            if user_profile.role == 1:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user   = self.request.user
        if not self.user_passes_test(request):
            suspicious_user_filter = Suspicious.objects.filter(user=instance_user)
            if suspicious_user_filter.exists():
                suspicious_user_instance    = suspicious_user_filter.first()
                current_attempt             = suspicious_user_instance.attempt
                total_attempt               = current_attempt + 1
                update_time                 = datetime.datetime.now()
                suspicious_user_filter.update(attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR, 
                "You are not allowed. Your account is being tracked for suspicious activity !"
            )
            return HttpResponseRedirect(reverse('home'))
        return super(DateCreateView, self).dispatch(request, *args, **kwargs)