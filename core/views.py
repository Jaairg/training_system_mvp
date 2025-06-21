from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.forms import *
from datetime import datetime

def redirect_to_custom_page(profile, trainee_id):
    if profile.role.role_name == "Trainer":
        return redirect(f'/trainer/?tab=trainee_itp&user_id={trainee_id}')  # Redirect to trainer dashboard once form it's saved
    elif profile.role.role_name == "Supervisor":
        return redirect(f'/supervisor/?tab=trainee_itp&user_id={trainee_id}')
    return HttpResponse("Unauthorized", status=401)

def sign_itp(itp_id, profile, trainee_id):
    itp = ITP.objects.get(pk=itp_id)  # Identify the specific ITP being updated
    if profile == itp.trainer:  # Securing the action so only the trainer can sign
        itp.trainer_signature = True  # Updates the trainer_signature value once the checkbox is marked
        if not itp.completion_date:
            itp.completion_date = datetime.now()
        itp.save()  # Commit the information to the database
        return redirect_to_custom_page(profile, trainee_id)
    return None

def tabs_redirect(valid_tabs, request):
    tab = request.GET.get('tab', 'dashboard') # Dashboard is the default page
    if tab not in valid_tabs:
        tab ='dashboard'
    return tab

def get_trainee_itp(request, profile):
    trainee_itp = None
    trainee = None
    try:
        trainee_id = int(request.GET.get('user_id'))
    except (TypeError, ValueError):
        trainee_id = None
    if trainee_id is not None:
        trainee = Users.objects.filter(pk=trainee_id).first()
        if trainee:
            trainee_itp=ITP.objects.filter(trainer=profile, trainee__profile_id=trainee.profile_id)
    return trainee, trainee_itp, trainee_id

def validate_trainee_itp(request, profile):
    trainee, trainee_itp, trainee_id = get_trainee_itp(request, profile)
    if 'user_id' in request.GET:
        if trainee_id is None:
            return HttpResponse("Invalid or missing trainee ID.", status=400)
        if not trainee or not trainee_itp:
            return HttpResponse("Trainee or ITP not found.", status=400)
    return trainee, trainee_itp, trainee_id

@login_required
def trainee_view(request):
    profile = request.user.profile  # get the linked Users record

    trainee_itps = ITP.objects.filter(trainee=profile)  # only ITPs where this user is the trainee

    if profile.role.role_name != 'Trainee':
        return HttpResponse("You are not authorized to access this page")

    valid_tabs =['dashboard', 'my_itps']
    tab = tabs_redirect(valid_tabs, request)

    if request.method == "POST":
        itp_id = request.POST.get('itp')
        itp = ITP.objects.get(itp_id=itp_id)
        if profile == itp.trainee:
            if itp.trainer_signature is True: # If trainer signature in the form received is true will allow to update the trainee signature
                itp.trainee_signature = True
                itp.save()
                return redirect("/trainee/?tab=my_itps")

    return render(request, 'trainee_view.html', {
        'profile': profile,
        'active_tab': tab,
        'itps': trainee_itps,
    })

@login_required
def trainer_view(request):
    profile = request.user.profile

    if profile.role.role_name != 'Trainer':
        return HttpResponse("You are not authorized to access this page")

    trainees_list = Users.objects.filter(profile_id__in=ITP.objects.filter(trainer=profile).values_list('trainee_id', flat=True))

    trainer_itp_exist = ITP.objects.filter(trainee=profile).exists() # It checks if the current user  (profile) is listed as trainee in any ITP
    trainer_itps = ITP.objects.filter(trainee=profile) # Get the trainer ITPs

    result = validate_trainee_itp(request, profile)
    if isinstance(result, HttpResponse):
        return result
    trainee, trainee_itp, trainee_id = result

    valid_tabs =['dashboard', 'my_trainees', 'my_itps', 'trainee_itp']
    tab = tabs_redirect(valid_tabs, request)

    if request.method == "POST":
        itp_id = request.POST.get('itp') # Get the submitted ITP ID
        return sign_itp(itp_id, profile, trainee_id)

    return render(request, 'trainer_view.html',{
        'active_tab': tab,
        'profile': profile,
        'trainer_itp_exist': trainer_itp_exist,
        'itps': trainer_itps,
        'my_trainees_list': trainees_list,
        'trainee_itp': trainee_itp,
        'trainee': trainee
    })

@login_required()
def supervisor_view(request):
    profile = request.user.profile

    if profile.role.role_name != 'Supervisor':
        return HttpResponse("You are not authorized to access this page")

    valid_tabs =['dashboard', 'my_trainees', 'trainee_itp', 'my_itps','workcenter_members', 'mtl_management']
    tab = tabs_redirect(valid_tabs, request)

    trainees_list = Users.objects.filter(profile_id__in=ITP.objects.filter(trainer=profile).values_list('trainee_id', flat=True))

    result = validate_trainee_itp(request, profile)
    if isinstance(result, HttpResponse):
        return result
    trainee, trainee_itp, trainee_id = result

    supervisor_itp_exist = ITP.objects.filter(trainee=profile).exists()
    supervisor_itps = ITP.objects.filter(trainee=profile)
    workcenter_members = Users.objects.filter(workcenter=profile.workcenter).exclude(pk=profile.pk)
    workcenter_mtl = MTL.objects.filter(workcenter=profile.workcenter)

    if request.method == "POST":
        itp_id = request.POST.get('itp') # Get the submitted ITP ID
        return sign_itp(itp_id, profile)

    return render(request, 'supervisor_view.html',{
        'profile': profile,
        'active_tab': tab,
        'my_trainees_list': trainees_list,
        'trainee_itp': trainee_itp,
        'trainee': trainee,
        'supervisor_itp_exists': supervisor_itp_exist,
        'itps': supervisor_itps,
        'workcenter_members' : workcenter_members,
        'workcenter_tasks' : workcenter_mtl
    })

def custom_redirect_view(request):
    if request.user.is_authenticated:
        role = request.user.profile.role.role_name #Check the role of the user request
        if role == "Trainee":
            return redirect('trainee_view') # If user is Trainee and trying to access this redirects to my_itps path
        elif role == "Trainer":
            return redirect('trainer_view') # If user is Trainer and trying to access this redirects to trainer path
        else:
            return redirect('supervisor_view')
    else:
        return redirect('login')

def create_form_view(request):
    profile = request.user.profile

    if profile.role.role_name == "Trainee": # If a user is trainee try to access it gets blocked
        return HttpResponse("You are not authorized to access this page")

    # Create a blank form and send it to template
    # Load form with request.POST
    form = ITPForm(request.POST or None)

    # This query set allows to filter trainees and trainers for the same dropdown excluding the profile that is requesting,
    form.fields['trainee'].queryset = Users.objects.filter(workcenter=profile.workcenter, role__role_name__in=["Trainee", "Trainer"],
                                                           rank__rank_level__lt=profile.rank.rank_level).exclude(pk=profile.pk)
    form.fields['mtl'].queryset = MTL.objects.filter(workcenter=profile.workcenter)

    if request.method =='POST':
        if form.is_valid(): # Validate the form
            itp = form.save(commit=False) # Create, but don't save the new itp instance.
            itp.trainer = request.user.profile # Set trainer
            itp.trainer_signature = False
            itp.trainee_signature = False
            itp.save() # Save the form
            return redirect_to_custom_page(profile)

    return render(request, 'create_form.html', {'form': form})

def add_tasks(request):
    profile = request.user.profile

    if profile.role.role_name != 'Supervisor':
        return HttpResponse("You are not authorized to access this page")

    form = MTLForm(request.POST, workcenter=profile.workcenter)

    form.fields['cfetp'].queryset = CFETP.objects.order_by('task_number').exclude(mtl__workcenter=profile.workcenter)

    if request.method == 'POST':
        if form.is_valid():
            mtl = form.save(commit=False)
            mtl.workcenter = profile.workcenter
            mtl.save()
            return redirect('/supervisor/?tab=mtl_management')

    return render(request, 'mtl_form.html',{
        'form':form
    })

def edit_user_view(request, user_id):
    profile = request.user.profile

    if profile.role.role_name != 'Supervisor':
        return HttpResponse("You are not authorized to access this page")

    user_to_edit = Users.objects.get(pk=user_id)

    form = ProfileForm(request.POST or None)

    if profile.workcenter == user_to_edit.workcenter:
        user_skill_level = user_to_edit.skill_level

        # TODO: Confirm if demotion are allowed
        form.fields['rank'].queryset = Ranks.objects.order_by('rank_level').exclude(users__rank_id=user_to_edit.rank_id)
        if user_skill_level >= 5 :
            form.fields['role'].queryset = Roles.objects.filter(role_name__in=['Trainer', 'Trainee'])
        else:
            form.fields['role'].queryset = Roles.objects.filter(role_name__in=['Trainee'])

        form.fields['skill_level'].queryset = Users.objects

        if request.method == 'POST':
            if form.is_valid():
                user = form.save(commit=False)
                user.profile_id = user_to_edit.profile_id
                user.name = user_to_edit.name
                user.workcenter = profile.workcenter
                user.afsc = user_to_edit.afsc
                user.save()
                return redirect('/supervisor/?tab=workcenter_members')

    return render(request, 'edit_user.html', {
        'form': form,
        'profile': user_to_edit
    })
