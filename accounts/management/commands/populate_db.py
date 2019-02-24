from django.core.management.base import BaseCommand
# from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Faculty, UserProfile

# https://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database


# $ python manage.py populate_db
class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Seeding Fake User Data'




    # Create Faculties
    def _create_faculties(self):
        if not Faculty.objects.filter(code__iexact='IT').exists():
            f_it = Faculty(code='IT', title='Information & Technology')
            f_it.save()

        if not Faculty.objects.filter(code__iexact='EEE').exists():
            f_eee = Faculty(code='EEE', title='Electrical & Electronics Engineering')
            f_eee.save()

        if not Faculty.objects.filter(code__iexact='CSE').exists():
            f_cse = Faculty(code='CSE', title='Computer Science & Engineering')
            f_cse.save()

        if not Faculty.objects.filter(code__iexact='SWE').exists():
            f_sw = Faculty(code='SWE', title='Software Engineering')
            f_sw.save()




    # Create Users
    def _create_users(self):
        # University Administrator
        if not User.objects.filter(username__iexact='MM').exists():
            u_mm = User(username='MM', email='mm@test.com', password='test12345')
            u_mm.save()

        if not User.objects.filter(username__iexact='AD').exists():
            u_ad = User(username='AD', email='ad@test.com', password='test12345')
            u_ad.save()

        # ------------------- Faculty Specific User -------------------
        # IT Department
        if not User.objects.filter(username__iexact='MC_IT').exists():
            u_mc_it = User(username='MC_IT', email='mc_it@test.com', password='test12345')
            u_mc_it.save()

        if not User.objects.filter(username__iexact='FG_IT').exists():
            u_fg_it = User(username='FG_IT', email='fg_it@test.com', password='test12345')
            u_fg_it.save()

        if not User.objects.filter(username__iexact='ST_IT').exists():
            u_st_it = User(username='ST_IT', email='st_it@test.com', password='test12345')
            u_st_it.save()

        # CSE Department
        if not User.objects.filter(username__iexact='MC_CSE').exists():
            u_mc_cse = User(username='MC_CSE', email='mc_cse@test.com',
                         password='test12345')
            u_mc_cse.save()

        if not User.objects.filter(username__iexact='FG_CSE').exists():
            u_fg_cse = User(username='FG_CSE', email='fg_cse@test.com',
                       password='test12345')
            u_fg_cse.save()

        if not User.objects.filter(username__iexact='ST_CSE').exists():
            u_st_cse = User(username='ST_CSE', email='st_cse@test.com',
                       password='test12345')
            u_st_cse.save()

        # EEE Department
        if not User.objects.filter(username__iexact='MC_EEE').exists():
            u_mc_eee = User(username='MC_EEE', email='mc_eee@test.com',
                         password='test12345')
            u_mc_eee.save()

        if not User.objects.filter(username__iexact='FG_EEE').exists():
            u_fg_eee = User(username='FG_EEE', email='fg_eee@test.com',
                       password='test12345')
            u_fg_eee.save()

        if not User.objects.filter(username__iexact='ST_EEE').exists():
            u_st_eee = User(username='ST_EEE', email='st_eee@test.com',
                       password='test12345')
            u_st_eee.save()




    # Update User Profiles
    def _update_user_profiles(self):
        # University Administrator
        mm_filter = UserProfile.objects.filter(user__username__iexact='MM')
        if mm_filter.exists():
            mm_filter.update(role=0, faculty=None)

        ad_filter = UserProfile.objects.filter(user__username__iexact='AD')
        if ad_filter.exists():
            ad_filter.update(role=1, faculty=None)

        # ------------------- Faculty Specific User -------------------
        # IT Department
        qs_it = Faculty.objects.filter(code__iexact='IT')
        if qs_it.exists():
            f_it = qs_it.first()

            mc_it_filter = UserProfile.objects.filter(user__username__iexact='MC_IT')
            if mc_it_filter.exists():
                mc_it_filter.update(role=2, faculty=f_it)

            fg_it_filter = UserProfile.objects.filter(user__username__iexact='FG_IT')
            if fg_it_filter.exists():
                fg_it_filter.update(role=3, faculty=f_it)

            st_it_filter = UserProfile.objects.filter(user__username__iexact='ST_IT')
            if st_it_filter.exists():
                st_it_filter.update(role=4, faculty=f_it)

        # CSE Department
        qs_cse = Faculty.objects.filter(code__iexact='CSE')
        if qs_cse.exists():
            f_cse = qs_cse.first()

            mc_cse_filter = UserProfile.objects.filter(user__username__iexact='MC_CSE')
            if mc_cse_filter.exists():
                mc_cse_filter.update(role=2, faculty=f_cse)

            fg_cse_filter = UserProfile.objects.filter(user__username__iexact='FG_CSE')
            if fg_cse_filter.exists():
                fg_cse_filter.update(role=3, faculty=f_cse)

            st_cse_filter = UserProfile.objects.filter(user__username__iexact='ST_CSE')
            if st_cse_filter.exists():
                st_cse_filter.update(role=4, faculty=f_cse)

        # EEE Department
        qs_eee = Faculty.objects.filter(code__iexact='EEE')
        if qs_eee.exists():
            f_eee = qs_eee.first()

            mc_eee_filter = UserProfile.objects.filter(user__username__iexact='MC_EEE')
            if mc_eee_filter.exists():
                mc_eee_filter.update(role=2, faculty=f_eee)

            fg_eee_filter = UserProfile.objects.filter(user__username__iexact='FG_EEE')
            if fg_eee_filter.exists():
                fg_eee_filter.update(role=3, faculty=f_eee)

            st_eee_filter = UserProfile.objects.filter(user__username__iexact='ST_EEE')
            if st_eee_filter.exists():
                st_eee_filter.update(role=4, faculty=f_eee)


    def handle(self, *args, **options):
        self._create_faculties()
        self._create_users()
        self._update_user_profiles()
