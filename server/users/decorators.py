from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def tenant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='units'):
    '''
    Decorator for views that checks that the logged in user is a tenant,
    redirects to the landlord page if not.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_tenant(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def landlord_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='dashboard'):
    '''
    Decorator for views that checks that the logged in user is a landlord,
    redirects to the tenant dashboard if not page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_landlord(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
