from django.shortcuts import render, redirect

from .models import Job
from .forms import JobForm

# Create your views here.


def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jobs:job_listing')
    else:
        form = JobForm()

        # If form is invalid, print errors
    if form.errors:
        print(form.errors)
    return render(request, 'jobs/create_job.html', {'form': form})


def job_listing(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_listing.html', {'jobs': jobs})

