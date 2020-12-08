
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_staff = None
    is_superuser = None

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'authenticate'


class Item(models.Model):
    title = models.CharField(max_length=500)
    price = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    publish_date = models.CharField(max_length=15)
    publisher = models.CharField(max_length=100)
    publisher_mobile = models.CharField(max_length=15)
    description = models.TextField()
    square = models.CharField(max_length=20)
    direction = models.CharField(max_length=50)
    policy = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_data'


class DeletedItem(models.Model):
    deleted_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    price = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    publish_date = models.CharField(max_length=15)
    publisher = models.CharField(max_length=100)
    publisher_mobile = models.CharField(max_length=15)
    description = models.TextField()
    square = models.CharField(max_length=20)
    direction = models.CharField(max_length=50)
    policy = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    deleted_date = models.DateTimeField(auto_now_add=True)
    deleted_user = models.ForeignKey(
        'User', related_name='fk_deleted_user', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_deleted_data'


class SystemConfig(models.Model):
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    total_page = models.IntegerField()
    created_user = models.CharField(max_length=50)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_system_config'


class LogCrawl(models.Model):
    log_id = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_log_crawl'
