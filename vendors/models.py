from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_email
from food_online.settings import INSTALLED_APPS


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendors/licenses')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None: # If record is being updated
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                if self.is_approved:
                    mail_subject = 'Congratulations! Your foodOnline Restaurant has been Approved.'
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    send_email(mail_subject, mail_template, context)
                else:
                    mail_subject = 'foodOnline Restauratn Denied'
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    send_email(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)