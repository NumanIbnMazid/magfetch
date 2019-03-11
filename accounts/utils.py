import random
import string
import time
from django.utils.text import slugify


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_number_generator(size=3, chars='1234567890'):
    return ''.join(random.choice(chars) for _ in range(size))

def time_str_mix_slug():
    timestamp_y     = time.strftime("%Y")
    timestamp_m     = time.strftime("%m")
    timestamp_d     = time.strftime("%d")
    timestamp_now   = time.strftime("%H%M%S")
    random_str      = random_string_generator()
    random_num      = random_number_generator()
    bindings        = (
        random_num + timestamp_d + random_str +
        timestamp_y + timestamp_now + timestamp_m
    )
    return bindings


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

