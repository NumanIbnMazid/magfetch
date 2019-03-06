import os
import time
import random
import string
from django.conf import settings
# from django.utils.text import slugify
# from accounts.models import UserProfile


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_contribution_path(instance, filename):
    new_filename = "{user}_{type}-{category}-{title}-{datetime}".format(
        user=instance.user,
        type=instance.category.category_for,
        category=instance.category,
        title=instance.title,
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    if instance.category.category_for == 0:
        return "user_{0}/documents/{final_filename}".format(
            instance.user,
            final_filename=final_filename
        )
    if instance.category.category_for == 1:
        return "user_{0}/images/{final_filename}".format(
            instance.user,
            final_filename=final_filename
        )
    return "user_{0}/{final_filename}".format(
        instance.user,
        final_filename=final_filename
    )

    

def random_string_generator(size=3, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=3, chars='1234567890'):
    return ''.join(random.choice(chars) for _ in range(size))
    

# def slug_generator(instance, new_slug=None):
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.document)

#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=4)
#         )
#         return slug_generator(instance, new_slug=new_slug)
#     return slug
