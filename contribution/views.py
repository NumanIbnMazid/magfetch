from django.shortcuts import render, redirect, get_object_or_404
# Models Import
from .models import ContributionCategory, Contribution, Comment
from accounts.models import UserProfile
from system_data.models import Date
from suspicious.models import Suspicious
# Form import
from .forms import (
    ContributionCategoryCreateForm,
    ContributionUploadForm,
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
from .handlers import create_notification_to_mc_upload
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse




# Contribution Category Create View
@method_decorator(login_required, name='dispatch')
class ContributionCategoryCreateView(CreateView):
    template_name = 'category/create.html'
    form_class = ContributionCategoryCreateForm

    def form_valid(self, form):
        title = form.instance.title
        category_for = form.instance.category_for
        # category_for = form.instance.category_for
        qs = ContributionCategory.objects.filter(
            title__iexact=title, category_for=category_for)
        if qs.exists():
            form.add_error(
                'title', forms.ValidationError(
                    "This Category is alreay exists! Please try another one."
                )
            )
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 "Category has been added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contribution:category_create')

    def get_context_data(self, **kwargs):
        context = super(ContributionCategoryCreateView,
                        self).get_context_data(**kwargs)
        doc_category = ContributionCategory.objects.filter(
            category_for=0).order_by('-created_at')
        img_category = ContributionCategory.objects.filter(
            category_for=1).order_by('-created_at')
        context['doc_categories'] = doc_category
        context['doc_categories_count'] = doc_category.count()
        context['img_categories'] = img_category
        context['img_categories_count'] = img_category.count()
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
        return super(ContributionCategoryCreateView, self).dispatch(request, *args, **kwargs)


# Contribution Category Update View
@method_decorator(login_required, name='dispatch')
class ContributionCategoryUpdateView(UpdateView):
    template_name = 'category/update.html'
    form_class = ContributionCategoryCreateForm

    def get_object(self):
        slug = self.kwargs['slug']
        qs = ContributionCategory.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        pre = self.get_object()
        title = form.instance.title
        category_for = form.instance.category_for
        if not pre.title == title:
            qs = ContributionCategory.objects.filter(
                title__iexact=title, category_for=category_for)
            if qs.exists():
                form.add_error(
                    'title', forms.ValidationError(
                        "This Category is alreay exists! Please try another one."
                    )
                )
                return super().form_invalid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             "Category has been added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contribution:category_create')

    def get_context_data(self, **kwargs):
        context = super(ContributionCategoryUpdateView,
                        self).get_context_data(**kwargs)
        doc_category = ContributionCategory.objects.filter(
            category_for=0).order_by('-created_at')
        img_category = ContributionCategory.objects.filter(
            category_for=1).order_by('-created_at')
        context['doc_categories'] = doc_category
        context['doc_categories_count'] = doc_category.count()
        context['img_categories'] = img_category
        context['img_categories_count'] = img_category.count()
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
        return super(ContributionCategoryUpdateView, self).dispatch(request, *args, **kwargs)


# Contribution Category Delete View
@method_decorator(login_required, name='dispatch')
class ContributionCategoryDeleteView(DeleteView):
    template_name = 'category/delete.html'
    form_class = ContributionCategoryCreateForm

    def get_object(self):
        slug = self.kwargs['slug']
        qs = ContributionCategory.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Category has been deleted successfully!")
        return reverse('contribution:category_create')

    def get_context_data(self, **kwargs):
        context = super(ContributionCategoryDeleteView,
                        self).get_context_data(**kwargs)
        doc_category = ContributionCategory.objects.filter(
            category_for=0).order_by('-created_at')
        img_category = ContributionCategory.objects.filter(
            category_for=1).order_by('-created_at')
        context['doc_categories'] = doc_category
        context['doc_categories_count'] = doc_category.count()
        context['img_categories'] = img_category
        context['img_categories_count'] = img_category.count()
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
        return super(ContributionCategoryDeleteView, self).dispatch(request, *args, **kwargs)




# Contribution Upload View
@method_decorator(login_required, name='dispatch')
class ContributionUploadView(CreateView):
    template_name = 'contribution/upload.html'
    form_class = ContributionUploadForm

    def form_valid(self, form):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user).first()
        # Form Data
        title = form.instance.title
        qs = Contribution.objects.filter(title__iexact=title, user=profile)
        if qs.exists():
            form.add_error(
                'title', forms.ValidationError(
                    "You already have submitted a contribution with this name! Please try another one."
                )
            )
            return super().form_invalid(form)
        # Model Field Data Insertion
        form.instance.user = profile
        file = form.save().file
        base_name = os.path.basename(file.name)
        # form.instance.slug = os.path.splitext(base_name)[0]
        messages.add_message(self.request, messages.SUCCESS,
                             "Your article has been uploaded successfully!!!")
        new_object = form.save()
        # Notification Create
        slug = new_object.slug
        category = new_object.category
        uploaded_at = new_object.created_at
        message = "<strong>%s</strong> has uploaded a new Contribution.<br>Uploaded at: <strong>%s</strong><br>Category: <strong>%s</strong><br>Title: <strong>%s</strong>" % (
            profile.get_smallname(), uploaded_at.strftime('%a %H:%M  %d/%m/%y'), category, title)
        create_notification_to_mc_upload(profile, slug, message)
        # Sending Email
        mc_filter = UserProfile.objects.filter(role=2, faculty=profile.faculty)
        if mc_filter.exists():
            mail_msg = message
            mail_subject = '%s Uploaded a new Contribution.' % profile.get_smallname()
            mail_from = 'admin@magfetch.com'
            mail_text = 'Please do not Reply'
            if mc_filter.count() > 1:
                for mc in mc_filter:
                    subject = mail_subject
                    from_email = mail_from
                    to = ['%s' % mc.user.email]
                    text_content = mail_text
                    html_content = mail_msg
                    msg = EmailMultiAlternatives(
                        subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            else:
                mc = mc_filter.first()
                subject = mail_subject
                from_email = mail_from
                to = ['%s' % mc.user.email]
                text_content = mail_text
                html_content = mail_msg
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
        date_filter = Date.objects.filter(academic_year=today.year)
        if date_filter.exists():
            date = date_filter.first()
            submitted_contribution = Contribution.objects.filter(
                user=user, updated_at__year=today.year)
            if submitted_contribution.exists():
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
        return super(ContributionUploadView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ContributionListView(ListView):
    template_name = 'contribution/list.html'

    def get_queryset(self):
        user = UserProfile.objects.filter(user=self.request.user).first()
        query = Contribution.objects.filter(user__faculty=user.faculty).latest()
        return query

    def get_context_data(self, **kwargs):
        context = super(ContributionListView, self).get_context_data(**kwargs)
        user = UserProfile.objects.filter(user=self.request.user).first()
        faculty = user.faculty
        context['faculty'] = faculty
        context['faculty_code'] = faculty.code
        # contributions = Contribution.objects.filter(user__faculty=user.faculty)
        # for contribution in contributions:
        #     comments = contribution.user_contribution_file.all()
        #     context['comments'] = comments
        return context
    
    def user_passes_test(self, request):
        user = request.user
        if UserProfile.objects.filter(user=user).first().role == 2:
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
        return super(ContributionListView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ContributionDetailView(DetailView):
    template_name = 'contribution/detail.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Contribution.objects.get(slug=slug)
        except Contribution.DoesNotExist:
            raise Http404("Not Found !!!")
        except Contribution.MultipleObjectsReturned:
            qs = Contribution.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_context_data(self, **kwargs):
        context = super(ContributionDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        user_role = UserProfile.objects.filter(user=self.request.user).first().role
        qs = Comment.objects.filter(contribution__slug=self.object.slug)
        context['comments'] = qs
        if user_role == 0 or user_role == 1 or user_role == 2 or user_role == 3 or user_role == 7:
            context['custom_base'] = "base.html"
        else:
            context['custom_base'] = "landing-base.html"
        return context

    def user_passes_test(self, request):
        user = request.user
        user_role = UserProfile.objects.filter(user=user).first().role
        if user_role == 2 or user_role == 4 or user_role == 0 or user_role == 3:
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
        return super(ContributionDetailView, self).dispatch(request, *args, **kwargs)



@csrf_exempt
def contribution_delete(request):
    url = reverse('home')
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Contribution.objects.filter(slug=slug)
        if qs.exists():
            contribution = qs.first()
            if contribution.user.user == request.user:
                today = datetime.datetime.now()
                academic_year = Date.objects.filter(academic_year=str(today.year))
                if academic_year.exists():
                    closure_date = academic_year.first().closure_date
                    # today_format = today.strptime('2018-11-10 10:55:31', '%Y-%m-%d %H:%M:%S')
                    # print(closure_date)
                    # print(today_format)
                    if closure_date > today:
                        if contribution.is_selected == False:
                            qs.delete()
                            messages.add_message(request, messages.SUCCESS,
                                            "Contribution deleted successfully!"
                                            )
                            return redirect("/")
                        else:
                            messages.add_message(request, messages.WARNING,
                                            "You cannot delete this contribution as it has been selected for the magazine!"
                                            )
                    else:
                        messages.add_message(request, messages.WARNING,
                                            "Modification time has been expired ! You cannot delete this."
                                            )
            else:
                instance_user = request.user
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
                messages.add_message(request, messages.ERROR,
                                    "You are not allowed. Your account is being tracked for suspicious activity !"
                                    )
        else:
            messages.add_message(request, messages.WARNING,
                                 "Contribution Doesn't Exists!!!"
                                 )
    return HttpResponseRedirect(url)


@login_required
def mark_as_selected(request, slug):
    url = reverse('home')
    contribution_filter = Contribution.objects.filter(slug=slug)
    if contribution_filter.exists():
        contribution = contribution_filter.first()
        user_filter = UserProfile.objects.filter(user=request.user, role=2)
        if user_filter.exists() and user_filter.first().faculty == contribution.user.faculty:
            contribution_filter.update(
                is_selected = True
            )
            url = reverse('contribution:contribution_list')
            if request.method == 'POST':
                if not request.POST.get('default_comment') == "":
                    default_comment = request.POST.get('default_comment')
                    user_profile = user_filter.first()
                    comment = request.POST.get('comment')
                    if user_profile.role ==  2:
                        Comment.objects.create(contribution=contribution,commented_by=user_profile, comment=default_comment)
                        if user_profile.role ==  2:
                            contribution_filter.update(is_commented=True)
            messages.add_message(request, messages.SUCCESS,
                "Successfully marked as selected contribution!"
            )
        else:
            instance_user = request.user
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
            messages.add_message(request, messages.ERROR,
                                "You are not allowed. Your account is being tracked for suspicious activity !"
                                )
    else:
        messages.add_message(request, messages.WARNING,
                             "Contribution doesn't exists !!!")
    return HttpResponseRedirect(url)


@login_required
def mark_as_unselected(request, slug):
    url = reverse('home')
    contribution_filter = Contribution.objects.filter(slug=slug)
    if contribution_filter.exists():
        contribution = contribution_filter.first()
        user_filter = UserProfile.objects.filter(user=request.user, role=2)
        if user_filter.exists() and user_filter.first().faculty == contribution.user.faculty:
            contribution_filter.update(
                is_selected=False
            )
            url = reverse('contribution:contribution_list')
            messages.add_message(request, messages.SUCCESS,
                                 "Successfully removed from selected contribution!"
                                 )
        else:
            instance_user = request.user
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
            messages.add_message(request, messages.ERROR,
                                    "You are not allowed. Your account is being tracked for suspicious activity !"
                                    )
    else:
        messages.add_message(request, messages.WARNING,
                             "Contribution doesn't exists !!!")
    return HttpResponseRedirect(url)


@login_required
def comment_create(request, slug):
    url = reverse('home')
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.filter(user=user).first()
        comment = request.POST.get('comment')
        comment_area = request.POST.get('comment_area')
        if user_profile.role ==  2 or user_profile.role == 4:
            contribution_qs = Contribution.objects.filter(slug=slug)
            if contribution_qs.exists():
                contribution = contribution_qs.first()
                Comment.objects.create(contribution=contribution,commented_by=user_profile, comment=comment)
                # messages.add_message(request, messages.SUCCESS, "Commented successfully!")
                if user_profile.role ==  2:
                    contribution_qs.update(is_commented=True)
                if comment_area == "absolute_comment":
                    url = reverse('contribution:comment_view', kwargs={'slug': slug})
                else:
                    url = reverse('contribution:contribution_detail', kwargs={'slug': slug})
            else:
                messages.add_message(request, messages.WARNING,
                             "Contribution doesn't exists !!!")
        else:
            instance_user = request.user
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
            messages.add_message(request, messages.ERROR,
                                    "You are not allowed. Your account is being tracked for suspicious activity !"
                                    )
    return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class CommentListView(ListView):
    template_name = 'contribution/comments/view.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        query = Comment.objects.filter(contribution__slug=slug)
        return query

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        context['contribution_slug'] = self.kwargs['slug']
        user_role = UserProfile.objects.filter(user=self.request.user).first().role
        if user_role == 0 or user_role == 1 or user_role == 2 or user_role == 3 or user_role == 7:
            context['custom_base'] = "base.html"
        else:
            context['custom_base'] = "landing-base.html"
        qs = Contribution.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            context['contribution'] = qs.first()
        return context

    def user_passes_test(self, request):
        slug = self.kwargs['slug']
        qs = Contribution.objects.filter(slug=slug)
        user = request.user
        user_profile = UserProfile.objects.filter(user=user).first()
        if qs.exists():
            contribution = qs.first()
            if contribution.user.faculty == user_profile.faculty:
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
        return super(CommentListView, self).dispatch(request, *args, **kwargs)





class SelectedContributionListView(ListView):
    template_name = 'contribution/selected_list.html'

    def get_queryset(self, *args, **kwargs):
        query = Contribution.objects.all().selected().latest()
        return query

    def get_context_data(self, **kwargs):
        context             = super(SelectedContributionListView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        context['file_urls'] = qs
        return context

    def user_passes_test(self, request):
        user = request.user
        user_role = UserProfile.objects.filter(user=user).first().role
        if user_role == 0 or user_role == 3:
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
        return super(SelectedContributionListView, self).dispatch(request, *args, **kwargs)