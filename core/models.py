# This is an auto-generated Django model module.
#   * Each model has one field with primary_key=True
#   * Each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


"""
    managed = False: tells Django: don’t try to create or modify this table.
    db_table: ensures Django uses the real table name.
    Check database access information in settings.py
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType

class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'Roles'

    def __str__(self):
        return self.role_name

class Ranks(models.Model):
    rank_id = models.AutoField(primary_key=True)
    rank_name = models.CharField(unique=True, max_length=100)
    rank_level = models.PositiveIntegerField(unique = True)

    class Meta:
        managed = True
        db_table = 'Ranks'

    def __str__(self):
        return f"{self.rank_name} -- {self.rank_level}"

class AFSC(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)

    class Meta:
        managed = True

    def __str__ (self):
        return f"{self.id} -- {self.code} -- {self.title}"

class Workcenter(models.Model):
    workcenter_id = models.AutoField(primary_key=True)
    workcenter_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'Workcenter'

    def __str__(self):
        return self.workcenter_name

class Users(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)

    name = models.CharField(max_length=100)
    skill_level = models.IntegerField(choices=[(3, "Apprentice"), (5, "Journeyman"), (7, "Craftsman"), (9, "Superintendent")])
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, blank=False, null=False)
    workcenter = models.ForeignKey('Workcenter',on_delete=models.SET_NULL, blank=True, null=True)
    rank = models.ForeignKey(Ranks, on_delete=models.PROTECT, blank=False, null=False)
    afsc = models.ForeignKey(AFSC, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'Users'

    def full_afsc(self):
        if self.afsc and self.skill_level:
            # Make sure 'x' exists in code before replacing
            if 'X' in self.afsc.code:
                return self.afsc.code.replace('X', str(self.skill_level))
            return f"{self.afsc.code}{self.skill_level}"
        return "N/A"

    def __str__(self):
        return f"{self.name} -- {self.get_skill_level_display()}"

class CFETP(models.Model):
    cfetp_id = models.AutoField(primary_key=True)
    task_number = models.CharField(max_length=35)
    cfetp_name = models.CharField(max_length=100)
    afsc = models.ForeignKey(AFSC, on_delete=models.CASCADE, null=False, blank=False)
    min_skill_level = models.IntegerField(choices=[(3, "Apprentice"), (5, "Journeyman"), (7, "Craftsman"), (9, "Superintendent")])

    class Meta:
        managed = True
        db_table = 'CFETP'

    def __str__(self):
        return self.cfetp_name

class MTL(models.Model):
    mtl_id = models.AutoField(primary_key=True)
    workcenter = models.ForeignKey(Workcenter, models.DO_NOTHING, null=True)
    cfetp = models.ForeignKey(CFETP, models.DO_NOTHING, null=True)

    class Meta:
        managed = True
        db_table = 'MTL'

    def __str__(self):
        return f"{self.cfetp.task_number} -- {self.cfetp.cfetp_name}"

class ITP(models.Model):
    itp_id = models.AutoField(primary_key=True)
    trainee = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, related_name='trainee_itps')
    trainer = models.ForeignKey('Users', on_delete=models.SET_NULL, related_name='itp_trainer_set', blank=True, null=True)
    mtl = models.ForeignKey('MTL', models.DO_NOTHING, null=True)
    start_date = models.DateField(null=False)
    completion_date = models.DateField(blank=True, null=True)
    trainer_signature = models.BooleanField(default=False, blank=True, null=True)
    trainee_signature = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ITP'

    def __str__(self):
        return (f"{self.mtl.workcenter.workcenter_name} -- {self.mtl.cfetp.task_number} -- {self.mtl.cfetp.cfetp_name}"
                f" -- {self.trainer_signature} -- {self.trainee_signature}")


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
    content_type = models.ForeignKey(ContentType, models.DO_NOTHING)
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