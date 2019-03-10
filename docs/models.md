================== Models =================

# User
    - username          (CharField)
    - first_name        (CharField)
    - last_name         (CharField)
    - email             (EmailField)
    - password          (CharField)
    - groups            (ManyToManyField)       to - Group
    - user_permissions  (ManyToManyField)       to - Permission
    - is_staff          (BooleanField)
    - is_active         (BooleanField)
    - is_superuser      (BooleanField)
    - last_login        (DateTimeField)
    - date_joined       (DateTimeField)


# Faculty
    - code              (CharField)
    - title             (title)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# UserProfile
    - user              (OneToOneField)         to - user (profile)
    - slug              (SlugField)
    - role              (PositiveSmallIntegerField)
    - faculty           (ForeignKey)            to - Faculty (user_faculty)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)