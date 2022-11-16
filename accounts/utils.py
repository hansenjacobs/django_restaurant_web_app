from .models import User


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
