from .models import User
from django.core.exceptions import PermissionDenied


def get_user_dashboard(user):
    dashboards = {
        User.VENDOR: 'vendordashboard',
        User.CUSTOMER: 'customerdashboard',
    }

    dashbaord = None

    try:
        dashboard = dashboards[user.role]
    except:
        if user.is_superadmin:
            dashboard = '/admin'

    return dashboard


def user_is_customer(user):
    if user.role == User.CUSTOMER:
        return True
    else:
        raise PermissionDenied


def user_is_vendor(user):
    if user.role == User.VENDOR:
        return True
    else:
        raise PermissionDenied
