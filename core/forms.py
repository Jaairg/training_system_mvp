from django.forms import ModelForm
from django.utils import timezone
from core.models import *

# Using Django model forms to create the ITP form and get the info desired
class ITPForm(ModelForm):
    class Meta:
        model = ITP
        fields = ['trainee', 'mtl', 'start_date']

    def clean(self):
        cleaned_data = super().clean()
        trainee = cleaned_data.get('trainee')
        mtl = cleaned_data.get('mtl')
        itp = ITP.objects.filter(trainee=trainee, mtl=mtl)
        start_date = cleaned_data.get('start_date')

        errors={}
        if itp.exists():
            errors['trainee'] = ['An ITP with the selected MTL for this trainee already exist']
        if trainee.skill_level < mtl.cfetp.min_skill_level:
            errors['mtl'] = ['The selected MTL includes tasks that require a higher skill level than the trainee currently has. '
                                  'Please select an appropriate MTL or review the trainees skill level']
        if start_date < timezone.now().date():
            errors['start_date'] = ['The start date must be today or a future date. Past dates are not allowed']
        if errors:
            raise ValidationError(errors)

class MTLForm(ModelForm):
    class Meta:
        model = MTL
        fields = ['cfetp']

    def __init__(self, *args, **kwargs):
       self.workcenter = kwargs.pop('workcenter', None) # Get custom value for validation
       super().__init__(*args, **kwargs) # Django initialize the form normally

    def clean(self):
        cleaned_data = super().clean()
        cfetp = cleaned_data.get('cfetp')
        workcenter = self.workcenter
        mtl = MTL.objects.filter(cfetp=cfetp, workcenter=workcenter)

        if mtl.exists():
            raise ValidationError("Task already exists for this workcenter")

class ProfileForm(ModelForm):
    class Meta:
        model = Users
        fields = ['rank', 'role', 'skill_level']

    def clean(self):
        cleaned_data = super().clean()
        rank = cleaned_data.get('rank')
        skill_level = cleaned_data.get('skill_level')

        errors ={}
        if rank.rank_level < 4 and skill_level == 5:
            errors['skill_level'] = ['The selected skill level requires having at least Senior Airman rank level']
        if rank.rank_level < 5 and skill_level == 7:
            errors['skill_level'] = ['The selected skill level requires having at least Staff Sergeant rank level']
        if rank.rank_level < 8 and skill_level == 9:
            errors['skill_level'] = ['The selected skill level requires having at least Senior Master Sergeant rank level']

        if errors:
            raise ValidationError(errors)
