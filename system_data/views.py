from django.shortcuts import render
# Model imports
from .models import Date
from accounts.models import UserProfile
from suspicious.models import Suspicious
from utils.models import Announcement
# Form imports
from .forms import DateCreateForm
# Generic View imports
from django.views.generic import CreateView, UpdateView
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Other imports
from accounts.utils import time_str_mix_slug
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django import forms
import datetime

# ------------------------- Schedule/Date CreateView ---------------------------
@method_decorator(login_required, name='dispatch')
class DateCreateView(CreateView):
    template_name   = 'date/create.html'
    form_class      = DateCreateForm

    def form_valid(self, form):
        today       = datetime.date.today()
        next_year   = datetime.datetime(year=today.year+1, month=1, day=1)
        academic_year       = "%s-%s" %(today.strftime("%Y"), next_year.strftime("%Y")[-2:])
        status              = form.instance.status
        start_date          = form.instance.start_date
        closure_date        = form.instance.closure_date
        final_closure_date  = form.instance.final_closure_date
        validated_closure_date          = (start_date + datetime.timedelta(days=15))
        validated_final_closure_date    = (validated_closure_date + datetime.timedelta(days=14))
        # Validate Closure Date
        if not closure_date >= validated_closure_date:
            form.add_error(
                'closure_date', forms.ValidationError(
                    "Difference between Start Date and Closure Date must be at least 15 days!"
                    )
                )
            return super().form_invalid(form)
        # Validate Final Closure Date
        if not final_closure_date >= validated_final_closure_date:
            form.add_error(
                'final_closure_date', forms.ValidationError(
                    "Difference between Closure Date and Final Closure Date must be at least 14 days!"
                    )
                )
            return super().form_invalid(form)
        # Binding Academic Year
        form.instance.academic_year = "%s" % today.year
        # Sending Message if SUCCESS
        messages.add_message(self.request, messages.SUCCESS,
            "New Schedule has been created successfully !"
        )
        # Creating Announcement
        created_by  = UserProfile.objects.filter(user=self.request.user).first()
        category    = 'created_schedule'
        slug        = category + '-' + time_str_mix_slug()
        identifier  = 'created_schedule_%s' % today.year
        subject     = "New Schedule has been created for academic year %s" %(academic_year)
        message     = "Schedule for submitting contributions of academic year %s :<br> <strong>Start Date</strong>: %s <br> <strong>Closure Date</strong>: %s <br> <strong>Final Closure Date</strong>: %s <br> <hr>Submitting new contributions will start from <strong>Start Date</strong> and will continue until <strong>Closure Date</strong>. After <strong>Closure Date</strong> no new contributions will not be allowed to submit but submitted contributions can be updated until <strong>Final Closure Date</strong>.<hr>" %(academic_year,start_date.strftime("%m/%d/%Y %I:%M %p"),closure_date.strftime("%m/%d/%Y %I:%M %p"), final_closure_date.strftime("%m/%d/%Y %I:%M %p"))
        status      = status
        announcement_filter = Announcement.objects.filter(category__iexact=category, identifier__iexact=identifier)
        if announcement_filter.exists():
            announcement_filter.update(
                subject = subject,
                message = message,
                status  = status
            )
        else:
            Announcement.objects.create(
                created_by  = created_by,
                category    = category,
                slug        = slug,
                identifier  = identifier,
                subject     = subject,
                message     = message,
                status      = status
            )
        if status == 0:
            messages.add_message(self.request, messages.SUCCESS,
                "An Announcement has been created about the Schedule!"
            )
        else:
            messages.add_message(self.request, messages.WARNING,
                "Students will not be able to submit their contributions until you set the Publication Status as Published!"
            )
        # Returning Valid Form
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('system_data:date_update')

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
        today           = datetime.date.today()
        schedule_filter = Date.objects.filter(academic_year=today.year)
        if schedule_filter.exists():
            messages.add_message(self.request, messages.WARNING,
                "Already have a Schedule for this academic year! You cannot add more."
            )
            return HttpResponseRedirect(reverse('home'))
        if today.month == 12:
            messages.add_message(self.request, messages.WARNING,
                "New Schedule cannot be added on month December ! Please add New Schedule in next year."
            )
            return HttpResponseRedirect(reverse('home'))
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



# ------------------------- Schedule/Date UpdateView ---------------------------
@method_decorator(login_required, name='dispatch')
class DateUpdateView(UpdateView):
    template_name   = 'date/update.html'
    form_class      = DateCreateForm

    def get_object(self):
        today               = datetime.date.today()
        schedule_filter     = Date.objects.filter(academic_year=today.year)
        if schedule_filter.exists():
            try:
                schedule = Date.objects.get(academic_year=today.year)
            except Date.DoesNotExist:
                raise Http404("Not Found !!!")
            except Date.MultipleObjectsReturned:
                schedule    = schedule_filter.first()
            except:
                raise Http404("Something went wrong !!!")
        else:
            schedule = None
        return schedule

    def form_valid(self, form):
        today               = datetime.date.today()
        next_year           = datetime.datetime(year=today.year+1, month=1, day=1)
        academic_year       = "%s-%s" %(today.strftime("%Y"), next_year.strftime("%Y")[-2:])
        status              = form.instance.status
        start_date          = form.instance.start_date
        closure_date        = form.instance.closure_date
        final_closure_date  = form.instance.final_closure_date
        validated_closure_date          = (start_date + datetime.timedelta(days=15))
        validated_final_closure_date    = (validated_closure_date + datetime.timedelta(days=14))
        # Validate Closure Date
        if not closure_date >= validated_closure_date:
            form.add_error(
                'closure_date', forms.ValidationError(
                    "Difference between Start Date and Closure Date must be at least 15 days!"
                    )
                )
            return super().form_invalid(form)
        # Validate Final Closure Date
        if not final_closure_date >= validated_final_closure_date:
            form.add_error(
                'final_closure_date', forms.ValidationError(
                    "Difference between Closure Date and Final Closure Date must be at least 14 days!"
                    )
                )
            return super().form_invalid(form)
        # Checking Form Change
        pre             = self.get_object()
        if start_date != pre.start_date or closure_date != pre.closure_date or final_closure_date != pre.final_closure_date or status != pre.status:
            # Creating Announcement
            created_by  = UserProfile.objects.filter(user=self.request.user).first()
            category    = 'updated_schedule'
            slug        = category + '-' + time_str_mix_slug()
            identifier  = 'updated_schedule_%s' % today.year
            subject     = "Schedule has been updated for academic year %s" %(academic_year)
            message     = "Schedule for submitting contributions of academic year %s :<br> <strong>Start Date</strong>: %s <br> <strong>Closure Date</strong>: %s <br> <strong>Final Closure Date</strong>: %s <br> <hr>Submitting new contributions will start from <strong>Start Date</strong> and will continue until <strong>Closure Date</strong>. After <strong>Closure Date</strong> no new contributions will not be allowed to submit but submitted contributions can be updated until <strong>Final Closure Date</strong>.<hr>" %(academic_year,start_date.strftime("%m/%d/%Y %I:%M %p"),closure_date.strftime("%m/%d/%Y %I:%M %p"), final_closure_date.strftime("%m/%d/%Y %I:%M %p"))
            status      = status
            announcement_filter = Announcement.objects.filter(category__iexact=category, identifier__iexact=identifier)
            if announcement_filter.exists():
                announcement_filter.update(
                    subject = subject,
                    message = message,
                    status  = status,
                    updated_at = datetime.datetime.now()
                )
            else:
                Announcement.objects.create(
                    created_by  = created_by,
                    category    = category,
                    slug        = slug,
                    identifier  = identifier,
                    subject     = subject,
                    message     = message,
                    status      = status
                )
            if status == 0:
                messages.add_message(self.request, messages.SUCCESS,
                    "An Announcement has been created about the Schedule!"
                )
            else:
                messages.add_message(self.request, messages.WARNING,
                    "Students will not be able to submit their contributions until you set the Publication Status as Published!"
                )
            # Updating Satus of Created Announcement against Updated Announcement
            category_to_update    = 'created_schedule'
            identifier_to_update  = 'created_schedule_%s' % today.year
            announcement_filter = Announcement.objects.filter(category__iexact=category_to_update, identifier__iexact=identifier_to_update)
            if announcement_filter.exists():
                announcement_filter.update(
                    status  = status
                )
        # Returning Valid Form
        messages.add_message(self.request, messages.SUCCESS,
            "Schedule has been updated successfully !"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('system_data:date_update')

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
        today           = datetime.date.today()
        if today.month == 12:
            messages.add_message(self.request, messages.WARNING,
                "Schedule is not modifiable on month December!"
            )
            return HttpResponseRedirect(reverse('home'))
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
        return super(DateUpdateView, self).dispatch(request, *args, **kwargs)
