from django.shortcuts import render
# Models Import
from .models import DocumentCategory, Document, Image
from accounts.models import UserProfile
from system_data.models import Date
from suspicious.models import Suspicious
# Form import
from .forms import (
    DocumentCategoryCreateForm,
    DocumentUploadForm,
    ImageUploadForm
)
# generic view import
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
# other import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.paginator import Paginator
from django import forms
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from .handlers import create_notification_to_mc_upload
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
import os


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
        context = super(DocumentCategoryCreateView,
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
        context = super(DocumentCategoryUpdateView,
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
        document = form.save().document
        base_name = os.path.basename(document.name)
        form.instance.slug = os.path.splitext(base_name)[0]
        messages.add_message(self.request, messages.SUCCESS,
                             "Your article has been uploaded successfully!!!")
        new_object = form.save()
        # Delete Previous Uploads
        document_filter = Document.objects.filter(user=profile, category=new_object.category).exclude(slug=new_object.slug)
        if document_filter.exists():
            document_filter.delete()
        # Notification Create
        slug = new_object.slug
        category = new_object.category
        uploaded_at = new_object.created_at
        message = "%s has uploaded a new Document File.<br>Uploaded at: %s<br>Document Category: %s" %(
            profile.get_smallname(), uploaded_at, category)
        create_notification_to_mc_upload(profile, slug, message)
        # Sending Email
        mc_filter = UserProfile.objects.filter(role=2)
        if mc_filter.exists():
            if mc_filter.count() > 1:
                for mc in mc_filter:
                    subject = '%s Uploaded a new document.' % profile.get_smallname()
                    from_email = 'admin@magfetch.com'
                    to = ['%s' % mc.user.email]
                    text_content = 'Please do not Reply'
                    html_content = '<h4>Hi <i>%s</i></h4><strong>%s</strong> has uploaded a new Document File.<br>Uploaded at: <strong>%s</strong><br>Document Category: <strong>%s</strong>' % (
                        mc.get_smallname(), profile.get_smallname(), uploaded_at.strftime('%a %H:%M  %d/%m/%y'), category)
                    msg = EmailMultiAlternatives(
                        subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            else:
                mc = mc_filter.first()
                subject = '%s Uploaded a new document.' % profile.get_smallname()
                from_email = 'admin@magfetch.com'
                to = ['%s' % mc.user.email]
                text_content = 'Please do not Reply'
                html_content = '<h4>Hi <i>%s</i></h4><strong>%s</strong> has uploaded a new Document File.<br>Uploaded at: <strong>%s</strong><br>Document Category: <strong>%s</strong>' % (
                    mc.get_smallname(), profile.get_smallname(), uploaded_at.strftime('%a %H:%M  %d/%m/%y'), category)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

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
        user = UserProfile.objects.filter(user=instance_user).first()
        today = datetime.datetime.today()
        date_filter = Date.objects.filter(academic_year__iexact=today.year)
        if date_filter.exists():
            date = date_filter.first()
            submitted_document = Document.objects.filter(user=user, updated_at__year=today.year)
            if submitted_document.exists():
                submitted = True
            else:
                submitted = False
            if today > date.closure_date and submitted == False:
                messages.add_message(self.request, messages.ERROR,
                                        "Contribution submitting date has been expired! You are not allowed."
                                        )
                return HttpResponseRedirect(reverse('home'))
            if today > date.final_closure_date and submitted == True:
                messages.add_message(self.request, messages.ERROR,
                                     "Contribution submitting date has been expired! You are not allowed."
                                     )
                return HttpResponseRedirect(reverse('home'))
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


# Document List View
class DocumentListView(ListView):
    template_name = 'document/list.html'

    def get_queryset(self, *args, **kwargs):
        today = datetime.datetime.now()
        query = Document.objects.filter(updated_at__year=today.year)
        return query


# Image Upload View
@method_decorator(login_required, name='dispatch')
class ImageUploadView(CreateView):
    template_name = 'image/upload.html'
    form_class = ImageUploadForm

    def form_valid(self, form):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user).first()
        form.instance.user = profile
        image = form.save().image
        base_name = os.path.basename(image.name)
        form.instance.slug = os.path.splitext(base_name)[0]
        messages.add_message(self.request, messages.SUCCESS,
                             "Your image has been uploaded successfully!!!")
        new_object = form.save()
        # Delete Previous Uploads
        image_filter = Image.objects.filter(
            user=profile, title=new_object.title).exclude(slug=new_object.slug)
        if image_filter.exists():
            image_filter.delete()
        # Notification Create
        slug = new_object.slug
        title = new_object.title
        uploaded_at = new_object.created_at
        message = "%s has uploaded a new Image File.<br>Uploaded at: %s<br>Image Subject: %s" % (
            profile.get_smallname(), uploaded_at, title)
        create_notification_to_mc_upload(profile, slug, message)

        # Sending Email
        mc_filter = UserProfile.objects.filter(role=2)
        if mc_filter.exists():
            if mc_filter.count() > 1:
                for mc in mc_filter:
                    subject = '%s Uploaded a new image.' % profile.get_smallname()
                    from_email = 'admin@magfetch.com'
                    to = ['%s' % mc.user.email]
                    text_content = 'Please do not Reply'
                    html_content = '<h4>Hi <i>%s</i></h4><strong>%s</strong> has uploaded a new Image File.<br>Uploaded at: <strong>%s</strong><br>Image Subject: <strong>%s</strong>' % (
                        mc.get_smallname(), profile.get_smallname(), uploaded_at.strftime('%a %H:%M  %d/%m/%y'), title)
                    msg = EmailMultiAlternatives(
                        subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            else:
                mc = mc_filter.first()
                subject = '%s Uploaded a new document.' % profile.get_smallname()
                from_email = 'admin@magfetch.com'
                to = ['%s' % mc.user.email]
                text_content = 'Please do not Reply'
                html_content = '<h4>Hi <i>%s</i></h4><strong>%s</strong> has uploaded a new Image File.<br>Uploaded at: <strong>%s</strong><br>Image Category: <strong>%s</strong>' % (
                    mc.get_smallname(), profile.get_smallname(), uploaded_at.strftime('%a %H:%M  %d/%m/%y'), title)
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        
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
        user = UserProfile.objects.filter(user=instance_user).first()
        today = datetime.datetime.today()
        date_filter = Date.objects.filter(academic_year__iexact=today.year)
        if date_filter.exists():
            date = date_filter.first()
            submitted_image = Image.objects.filter(
                user=user, updated_at__year=today.year)
            if submitted_image.exists():
                submitted = True
            else:
                submitted = False
            if today > date.closure_date and submitted == False:
                messages.add_message(self.request, messages.ERROR,
                                     "Contribution submitting date has been expired! You are not allowed."
                                     )
                return HttpResponseRedirect(reverse('home'))
            if today > date.final_closure_date and submitted == True:
                messages.add_message(self.request, messages.ERROR,
                                     "Contribution submitting date has been expired! You are not allowed."
                                     )
                return HttpResponseRedirect(reverse('home'))
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
        return super(ImageUploadView, self).dispatch(request, *args, **kwargs)
