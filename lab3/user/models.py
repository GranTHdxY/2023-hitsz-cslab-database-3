# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CanteenInfo(models.Model):
    canteen_id = models.IntegerField(primary_key=True)
    canteen_name = models.CharField(max_length=20, blank=True, null=True)
    max_capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'canteen_info'


class CuisineInfo(models.Model):
    cuisine_id = models.IntegerField(primary_key=True)
    store = models.ForeignKey('StoreInfo', models.DO_NOTHING, blank=True, null=True)
    cuisine_name = models.CharField(max_length=20, blank=True, null=True)
    cuisine_price = models.FloatField(blank=True, null=True)
    cuisine_photo = models.TextField(blank=True, null=True)
    cuisine_comment = models.CharField(max_length=100, blank=True, null=True)
    cuisine_description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuisine_info'


class CustomerInfo(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_info'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ManagerInfo(models.Model):
    manager_id = models.IntegerField(primary_key=True)
    canteen = models.ForeignKey(CanteenInfo, models.DO_NOTHING, blank=True, null=True)
    manager_name = models.CharField(max_length=20, blank=True, null=True)
    manager_tel = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager_info'


class MerchatInfo(models.Model):
    merchant_id = models.IntegerField(primary_key=True)
    merchant_name = models.CharField(max_length=20, blank=True, null=True)
    merchant_tel = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'merchat_info'

class OrderInfo(models.Model):
    order_id = models.CharField(primary_key=True, max_length=10)
    customer = models.ForeignKey(CustomerInfo, models.DO_NOTHING, blank=True, null=True)
    payment_time = models.TimeField(blank=True, null=True)
    payment_mode = models.CharField(max_length=5, blank=True, null=True)
    order_state = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    total_cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_info'

class OrderContext(models.Model):
    order = models.ForeignKey('OrderInfo', models.DO_NOTHING)
    cuisine = models.ForeignKey(CuisineInfo, models.DO_NOTHING)
    cuisine_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_context'

class StoreInfo(models.Model):
    store_id = models.IntegerField(primary_key=True)
    canteen = models.ForeignKey(CanteenInfo, models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey(MerchatInfo, models.DO_NOTHING, blank=True, null=True)
    store_name = models.CharField(max_length=20, blank=True, null=True)
    store_comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_info'


class UserInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=10)
    customer = models.ForeignKey(CustomerInfo, models.DO_NOTHING, blank=True, null=True)
    manager = models.ForeignKey(ManagerInfo, models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey(MerchatInfo, models.DO_NOTHING, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    status = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    user_tel = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    user_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
