import os
import time
import random
import string
from django.utils.text import slugify
from accounts.models import UserProfile



def upload_document_path(instance, filename):
    return 'documents/user_{0}/{1}'.format(instance.user, filename)


def upload_image_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.user, filename)
    

def random_string_generator(size=3, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=3, chars='1234567890'):
    return ''.join(random.choice(chars) for _ in range(size))
    

def slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.document)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return slug_generator(instance, new_slug=new_slug)
    return slug
