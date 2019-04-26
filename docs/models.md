================== Choices =================
# User Roles:
    MARKETING_MANAGER       = 0
    ADMINISTRATOR           = 1
    MARKETING_COORDINATOR   = 2
    FACULTY_GUEST           = 3
    STUDENT                 = 4
    SITE_GUEST              = 7

# Date
    PUBLISHED   = 0
    UNPUBLISHED = 1

# Contribution Category
    DOCUMENT    = 0
    IMAGE       = 1

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

# Date
    - academic_year         (CharField)
    - start_date            (DateTimeField)
    - closure_date          (DateTimeField)
    - final_closure_date    (DateTimeField)
    - status                (PositiveSmallIntegerField)
    - created_at            (DateTimeField)
    - updated_at            (DateTimeField)

# Announcement
    - category          (CharField)
    - slug              (SlugField)
    - identifier        (CharField)
    - subject           (CharField)
    - message           (TextField)
    - status            (PositiveSmallIntegerField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# Notification
    - sender            (ForeignKey)                to - UserProfile (notification_sender)
    - receiver          (ForeignKey)                to - UserProfile (notification_receiver)
    - category          (CharField)
    - identifier        (CharField)
    - slug              (SlugField)
    - subject           (CharField)
    - message           (TextField)
    - has_read          (BooleanField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# ContributionCategory
    - category_for      (PositiveSmallIntegerField)
    - title             (CharField)
    - slug              (SlugField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# Contribution
    - user              (ForeignKey)            to - UserProfile (user_contribution)
    - title             (CharField)
    - file              (FileField)
    - category          (ForeignKey)            to - ContributionCategory (contribution_category)
    - slug              (SlugField)
    - is_commented      (BooleanField)
    - is_selected       (BooleanField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# Comment
    - contribution      (ForeignKey)            to - Contribution (user_contribution_file)
    - commented_by      (ForeignKey)            to - UserProfile (user_comment)
    - comment           (TextField)
    - is_special        (BooleanField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)

# Suspicious
    - user              (ForeignKey)            to - User (suspicious)
    - attempt           (PositiveSmallIntegerField)
    - first_attempt     (DateTimeField)
    - last_attempt      (DateTimeField)
    - ip                (CharField)
    - mac               (CharField)