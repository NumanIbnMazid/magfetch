from django.shortcuts import render
# Models Import 
from .models import DocumentCategory
from accounts.models import UserProfile
from system_data.models import Date
from suspicious.models import Suspicious
# Form import
from .forms import (
    DocumentCategoryCreateForm, 
    DocumentUploadForm
)
# generic view import
from django.views.generic import CreateView, UpdateView, DeleteView
# other import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.paginator import Paginator
from django import forms
from django.contrib import messages
import datetime


# Document Category Create View
@method_decorator(login_required, name='dispatch')
class DocumentCategoryCreateView(CreateView):
    template_name = 'document-category/create.html'
    form_class = DocumentCategoryCreateForm

    def form_valid(self, form):
        title = form.instance.title
        qs = DocumentCategory.objects.filter(title__iexact=title)
        if qs.exists():
            form.add_error(
                'title', forms.ValidationError(
                    "This Document Category is alreay exists! Please try another one."
                )
            )
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 "Document Category has been added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contribution:document_category_create')

    def get_context_data(self, **kwargs):
        context = super(DocumentCategoryCreateView, self).get_context_data(**kwargs)
        qs = DocumentCategory.objects.all().order_by('-created_at')
        paginator = Paginator(qs, 7)
        page = self.request.GET.get('page')
        categories = paginator.get_page(page)
        context['categories'] = categories
        context['categories_count'] = qs.count()
        return context

    def user_passes_test(self, request):
        user = request.user
        if UserProfile.objects.filter(user=user).first().role == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user   = self.request.user
        if not self.user_passes_test(request):
            suspicious_user = Suspicious.objects.filter(user=instance_user)
            if suspicious_user.exists():
                suspicious_user_instance    = Suspicious.objects.get(user=instance_user)
                current_attempt             = suspicious_user_instance.attempt
                total_attempt               = current_attempt + 1
                update_time                 = datetime.datetime.now()
                suspicious_user.update(attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR,
                "You are not allowed. Your account is being tracked for suspicious activity !"
            )
            return HttpResponseRedirect(reverse('home'))
        return super(DocumentCategoryCreateView, self).dispatch(request, *args, **kwargs)


# Document Category Update View
@method_decorator(login_required, name='dispatch')
class DocumentCategoryUpdateView(UpdateView):
    template_name = 'document-category/update.html'
    form_class = DocumentCategoryCreateForm

    def get_object(self):
        slug = self.kwargs['slug']
        qs = DocumentCategory.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        pre = self.get_object()
        title = form.instance.title
        if not pre.title == title:
            qs = DocumentCategory.objects.filter(title__iexact=title)
            if qs.exists():
                form.add_error(
                    'title', forms.ValidationError(
                        "This Document Category is alreay exists! Please try another one."
                    )
                )
                return super().form_invalid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             "Document Category has been added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contribution:document_category_create')

    def get_context_data(self, **kwargs):
        context = super(DocumentCategoryUpdateView,self).get_context_data(**kwargs)
        qs = DocumentCategory.objects.all().order_by('-created_at')
        paginator = Paginator(qs, 7)
        page = self.request.GET.get('page')
        categories = paginator.get_page(page)
        context['categories'] = categories
        context['categories_count'] = qs.count()
        return context

    def user_passes_test(self, request):
        user = request.user
        if UserProfile.objects.filter(user=user).first().role == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user = self.request.user
        if not self.user_passes_test(request):
            suspicious_user = Suspicious.objects.filter(user=instance_user)
            if suspicious_user.exists():
                suspicious_user_instance = Suspicious.objects.get(
                    user=instance_user)
                current_attempt = suspicious_user_instance.attempt
                total_attempt = current_attempt + 1
                update_time = datetime.datetime.now()
                suspicious_user.update(
                    attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR,
                                 "You are not allowed. Your account is being tracked for suspicious activity !"
                                 )
            return HttpResponseRedirect(reverse('home'))
        return super(DocumentCategoryUpdateView, self).dispatch(request, *args, **kwargs)


# Document Category Delete View
@method_decorator(login_required, name='dispatch')
class DocumentCategoryDeleteView(DeleteView):
    template_name = 'document-category/delete.html'
    form_class = DocumentCategoryCreateForm

    def get_object(self):
        slug = self.kwargs['slug']
        qs = DocumentCategory.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Document Category has been deleted successfully!")
        return reverse('contribution:document_category_create')

    def get_context_data(self, **kwargs):
        context = super(DocumentCategoryDeleteView,
                        self).get_context_data(**kwargs)
        qs = DocumentCategory.objects.all().order_by('-created_at')
        paginator = Paginator(qs, 7)
        page = self.request.GET.get('page')
        categories = paginator.get_page(page)
        context['categories'] = categories
        context['categories_count'] = qs.count()
        return context

    def user_passes_test(self, request):
        user = request.user
        if UserProfile.objects.filter(user=user).first().role == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user = self.request.user
        if not self.user_passes_test(request):
            suspicious_user = Suspicious.objects.filter(user=instance_user)
            if suspicious_user.exists():
                suspicious_user_instance = Suspicious.objects.get(
                    user=instance_user)
                current_attempt = suspicious_user_instance.attempt
                total_attempt = current_attempt + 1
                update_time = datetime.datetime.now()
                suspicious_user.update(
                    attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR,
                                 "You are not allowed. Your account is being tracked for suspicious activity !"
                                 )
            return HttpResponseRedirect(reverse('home'))
        return super(DocumentCategoryDeleteView, self).dispatch(request, *args, **kwargs)



# Document Upload View
@method_decorator(login_required, name='dispatch')
class DocumentUploadView(CreateView):
    template_name = 'document/upload.html'
    form_class = DocumentUploadForm

    def form_valid(self, form):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user).first()
        form.instance.user = profile
        messages.add_message(self.request, messages.SUCCESS,
                                "Your article has been uploaded successfully!!!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

    def user_passes_test(self, request):
        user = request.user
        if UserProfile.objects.filter(user=user).first().role == 4:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user = self.request.user
        date_filter = Date.objects.all()
        if date_filter.exists():
            today = datetime.datetime.today()
            date = date_filter.first()
            if today > date.closure_date:
                messages.add_message(self.request, messages.ERROR,
                                     "Contribution submitting date has been expired! You are not allowed."
                                     )
        else:
            messages.add_message(self.request, messages.ERROR,
                                 "No Schedule Added for collecting contributions for magazine! Please wait for the announcement."
                                 )
            return HttpResponseRedirect(reverse('home'))
        if not self.user_passes_test(request):
            suspicious_user = Suspicious.objects.filter(user=instance_user)
            if suspicious_user.exists():
                suspicious_user_instance = Suspicious.objects.get(
                    user=instance_user)
                current_attempt = suspicious_user_instance.attempt
                total_attempt = current_attempt + 1
                update_time = datetime.datetime.now()
                suspicious_user.update(
                    attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR,
                                 "You are not allowed. Your account is being tracked for suspicious activity !"
                                 )
            return HttpResponseRedirect(reverse('home'))
        return super(DocumentUploadView, self).dispatch(request, *args, **kwargs)
