from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET


from .models import Job
from .forms import JobForm

# Create your views here.


@require_GET
@require_POST
def create_job(request):
    form = JobForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("jobs:job_listing"))

    return render(request, "jobs/create_job.html", {"form": form})


@require_http_methods(["GET"])
def job_listing(request):
    jobs = Job.objects.filter(is_published=True)
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "jobs/job_listing.html", {"jobs": page_obj})


@require_http_methods(["GET"])
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    return render(request, "jobs/job_detail.html", {"job": job})
