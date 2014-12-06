from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
	def create_myuser(self, email, first_name, last_name='', password=None):
		"""
		create/save user
		"""
		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, password):
		"""
		Create/save a superuser
		"""
		user = self.create_user(email,
			first_name,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class MyUser(AbstractBaseUser):
	email = models.EmailField(max_length=255, verbose_name='Email address', unique=True)
	first_name = models.CharField(max_length=255, verbose_name='First name')
	last_name = models.CharField(max_length=255, verbose_name='Last name', blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date joined')


	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name']

	def get_full_name(self):
		return self.first_name + " " + self.last_name

	def __unicode__(self):
		return self.email

	@property
	def is_staff(self):
	    return self.is_admin
	
	@models.permalink
	def get_absolute_url(self):
		return ('detail', (), {'pk': self.id})
