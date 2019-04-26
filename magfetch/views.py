from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from accounts.models import UserProfile
from contribution.models import Contribution, Comment
from django.db.models import Q
import datetime

# @method_decorator(login_required, name='dispatch')
# class HomeView(TemplateView):
#     template_name = 'pages/home.html'


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        today = datetime.datetime.now()
        user_profile_filter = UserProfile.objects.filter(user=user)
        if user_profile_filter.exists():
            profile = user_profile_filter.first()
            # -------- Administrative Dashboard View -----------
            if profile.role == 0 or profile.role == 1 or profile.role == 2 or profile.role == 3:
                contributions = Contribution.objects.all().latest()
                contributors = UserProfile.objects.filter(~Q(user_contribution=None)).exclude(~Q(user_contribution__created_at__year=today.year))
                context = {
                    'contributions': contributions,
                    'contributions_this_year': contributions.contributions_this_year(),
                    'contributions_selected': contributions.selected().contributions_by_faculty(request.user.profile).contributions_this_year(),
                    'uncommented_contributions': contributions.uncommented().contributions_by_faculty(request.user.profile).contributions_this_year(),
                    'contributions_doc': contributions.contributions_doc().contributions_by_faculty(request.user.profile).contributions_this_year(),
                    'contributions_img': contributions.contributions_img().contributions_by_faculty(request.user.profile).contributions_this_year(),
                    'special_comments': contributions.filter(user_contribution_file__is_special=True).contributions_this_year(),
                    # All Contributions By Faculty
                    'IT_contributions_all': contributions.filter(user__faculty__code__iexact='IT'),
                    'CSE_contributions_all': contributions.filter(user__faculty__code__iexact='CSE'),
                    'SWE_contributions_all': contributions.filter(user__faculty__code__iexact='SWE'),
                    'EEE_contributions_all': contributions.filter(user__faculty__code__iexact='EEE'),
                    # All Contributions By Faculty within each year
                    'IT_contributions': contributions.filter(user__faculty__code__iexact='IT').contributions_this_year(),
                    'CSE_contributions': contributions.filter(user__faculty__code__iexact='CSE').contributions_this_year(),
                    'SWE_contributions': contributions.filter(user__faculty__code__iexact='SWE').contributions_this_year(),
                    'EEE_contributions': contributions.filter(user__faculty__code__iexact='EEE').contributions_this_year(),
                    # All Contributors By Faculty within each year
                    'IT_contributors': contributors.filter(faculty__code__iexact='IT'),
                    'CSE_contributors': contributors.filter(faculty__code__iexact='CSE'),
                    'SWE_contributors': contributors.filter(faculty__code__iexact='SWE'),
                    'EEE_contributors': contributors.filter(faculty__code__iexact='EEE'),
                    # MM Report
                    'contributions_selected_mm': contributions.selected().contributions_this_year(),
                    'uncommented_contributions_mm': contributions.uncommented().contributions_this_year(),
                    'special_comments_mm': contributions.filter(user_contribution_file__is_special=True).contributions_by_year(today.year),
                    'contributions_doc_mm': contributions.contributions_doc().contributions_this_year(),
                    'contributions_img_mm': contributions.contributions_img().contributions_this_year(),
                    # Extra
                    'input_value':today.year,
                    'contributions_by_year': contributions.contributions_by_year(today.year),
                    'contributions_by_year_faculty': contributions.contributions_by_year(today.year).contributions_by_faculty(request.user.profile),
                    'contributors_by_year': contributors
                }
                return render(request, "pages/home.html", context=context)
            # ------- Student Landing Page View -------
            if profile.role == 4:
                # If submited check
                submitted_filter = Contribution.objects.filter(
                    user=profile, updated_at__year=today.year)
                if submitted_filter.exists():
                    is_submitted = True
                else:
                    is_submitted = False
                context = {
                    'is_submitted': is_submitted,
                    'contributions': submitted_filter
                }
                return render(request, "landing/pages/home.html", context=context)
            # ------- Django Admin View -------
            if profile.user.is_staff == True:
                return render(request, "pages/home.html")
            # ------- Anonymous View -------
            if profile.role == 7:
                return render(request, "anonymous.html")
        return render(request, "anonymous.html")


def statistics_search(request):
    user = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    today = datetime.datetime.now()
    if user_profile_filter.exists():
        profile = user_profile_filter.first()
        # -------- Administrative Dashboard View -----------
        if profile.role == 0 or profile.role == 1 or profile.role == 2 or profile.role == 3:
            request_year = today.year
            if request.method == 'POST':
                request_year = request.POST.get('contribution_search')
            contributions = Contribution.objects.all().latest()
            contributors = UserProfile.objects.filter(~Q(user_contribution=None)).exclude(~Q(user_contribution__created_at__year=request_year))
            context = {
                'contributions': contributions,
                'contributions_this_year': contributions.contributions_this_year(),
                'contributions_selected': contributions.selected().contributions_by_faculty(request.user.profile).contributions_by_year(request_year),
                'uncommented_contributions': contributions.uncommented().contributions_by_faculty(request.user.profile).contributions_by_year(request_year),
                'contributions_doc': contributions.contributions_doc().contributions_by_faculty(request.user.profile).contributions_by_year(request_year),
                'contributions_img': contributions.contributions_img().contributions_by_faculty(request.user.profile).contributions_by_year(request_year),
                'special_comments': contributions.filter(user_contribution_file__is_special=True).contributions_by_year(request_year),
                # All Contributions By Faculty
                'IT_contributions_all': contributions.filter(user__faculty__code__iexact='IT'),
                'CSE_contributions_all': contributions.filter(user__faculty__code__iexact='CSE'),
                'SWE_contributions_all': contributions.filter(user__faculty__code__iexact='SWE'),
                'EEE_contributions_all': contributions.filter(user__faculty__code__iexact='EEE'),
                # All Contributions By Faculty within each year
                'IT_contributions': contributions.filter(user__faculty__code__iexact='IT').contributions_by_year(request_year),
                'CSE_contributions': contributions.filter(user__faculty__code__iexact='CSE').contributions_by_year(request_year),
                'SWE_contributions': contributions.filter(user__faculty__code__iexact='SWE').contributions_by_year(request_year),
                'EEE_contributions': contributions.filter(user__faculty__code__iexact='EEE').contributions_by_year(request_year),
                # All Contributors By Faculty within each year
                'IT_contributors': contributors.filter(faculty__code__iexact='IT'),
                'CSE_contributors': contributors.filter(faculty__code__iexact='CSE'),
                'SWE_contributors': contributors.filter(faculty__code__iexact='SWE'),
                'EEE_contributors': contributors.filter(faculty__code__iexact='EEE'),
                # MM Report
                'contributions_selected_mm': contributions.selected().contributions_by_year(request_year),
                'uncommented_contributions_mm': contributions.uncommented().contributions_by_year(request_year),
                'special_comments_mm': contributions.filter(user_contribution_file__is_special=True).contributions_by_year(request_year),
                'contributions_doc_mm': contributions.contributions_doc().contributions_by_year(request_year),
                'contributions_img_mm': contributions.contributions_img().contributions_by_year(request_year),
                # Extra
                'input_value':request_year,
                'contributions_by_year': contributions.contributions_by_year(request_year),
                'contributions_by_year_faculty': contributions.contributions_by_year(request_year).contributions_by_faculty(request.user.profile),
                'contributors_by_year': contributors
            }
            return render(request, "pages/home.html", context=context)
        # ------- Student Landing Page View -------
        if profile.role == 4:
            # If submited check
            submitted_filter = Contribution.objects.filter(
                user=profile, updated_at__year=today.year)
            if submitted_filter.exists():
                is_submitted = True
            else:
                is_submitted = False
            context = {
                'is_submitted': is_submitted,
                'contributions': submitted_filter
            }
            return render(request, "landing/pages/home.html", context=context)
        # ------- Django Admin View -------
        if profile.user.is_staff == True:
            return render(request, "pages/home.html")
        # ------- Anonymous View -------
        if profile.role == 7:
            return render(request, "anonymous.html")
    return render(request, "anonymous.html")