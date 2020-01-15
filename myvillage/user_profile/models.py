from django.db import models

# from __future__ import unicode_literals

from django.db import models
# from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):

    use_in_migrations = True

    def kreate_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self.kreate_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """creates and saves new super user with given details"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        user = self.kreate_user(email, password, **extra_fields)
        # user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)



class UserProfileModel(AbstractBaseUser, PermissionsMixin):
    """ represents the "user profile" in our system"""

    email = models.EmailField( unique=True )
    first_name = models.CharField( max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField( auto_now_add=True)
    is_active = models.BooleanField( default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    class Meta:
        unique_together = [['first_name', 'last_name']]

   

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        """ convert the object to a string"""
        return self.email

    