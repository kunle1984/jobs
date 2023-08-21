from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

# Decorators for job posting
def can_post(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is can post and 
    redirect to the login page if the user is not authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.can_post,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def is_super(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is can post and 
    redirect to the login page if the user is not authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator