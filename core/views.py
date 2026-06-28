from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmailLoginForm, ResumeSectionForm, SignupForm
from .models import Bullet, ResumeSection


def bullet_list(request):
    return render(request, 'bullet_list.html')


@login_required
def repository_view(request, section_id=None):
    sections = list(request.user.resume_sections.all())
    if not sections:
        default_names = ['Skills and Qualifications', 'Education', 'Work Experience', 'Projects', 'Volunteer']
        for position, name in enumerate(default_names):
            ResumeSection.objects.create(user=request.user, name=name, position=position)
        sections = list(request.user.resume_sections.all())

    active_section = None
    if section_id:
        active_section = get_object_or_404(ResumeSection, pk=section_id, user=request.user)
    elif sections:
        active_section = sections[0]

    form = ResumeSectionForm(instance=active_section)
    bullets = Bullet.objects.all()
    return render(request, 'repository.html', {
        'active_section': active_section,
        'bullets': bullets,
        'form': form,
        'sections': sections,
    })


@login_required
def add_section(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip() or 'Untitled section'
        next_position = request.user.resume_sections.count()
        section = ResumeSection.objects.create(user=request.user, name=name, position=next_position)
        messages.success(request, f'Added {section.name}.')
        return redirect('repository_section', section_id=section.id)
    return redirect('repository')


@login_required
def update_section(request, section_id):
    section = get_object_or_404(ResumeSection, pk=section_id, user=request.user)
    if request.method == 'POST':
        form = ResumeSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated.')
        else:
            messages.error(request, 'Please check the section details.')
    return redirect('repository_section', section_id=section.id)


@login_required
def delete_section(request, section_id):
    section = get_object_or_404(ResumeSection, pk=section_id, user=request.user)
    if request.method == 'POST':
        section_name = section.name
        section.delete()
        messages.success(request, f'Removed {section_name}.')
    return redirect('repository')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('repository')

    form = EmailLoginForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.user)
            return redirect('repository')
        messages.error(request, 'Please check your login details.')

    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('repository')

    form = SignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('repository')
        messages.error(request, 'Please fix the signup form errors.')

    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('bullet_list')
