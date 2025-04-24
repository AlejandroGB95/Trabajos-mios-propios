import hashlib
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import UrlMonitor

def index(request):
    urls = UrlMonitor.objects.all().order_by('has_changed', 'last_checked')
    return render(request, 'monitor/index.html', {'urls': urls})

def check_changes(request):
    urls = UrlMonitor.objects.all()
    for url_entry in urls:
        try:
            response = requests.get(url_entry.url, timeout=10)
            content = response.content
            new_hash = hashlib.md5(content).hexdigest()
            if url_entry.hash != new_hash:
                url_entry.has_changed = True
                url_entry.is_checked = False
                url_entry.hash = new_hash
            url_entry.last_checked = timezone.now()
            url_entry.save()
        except Exception as e:
            print(f"Error fetching {url_entry.url}: {e}")
    return redirect('index')

def mark_all_checked(request):
    UrlMonitor.objects.filter(has_changed=True, is_checked=False).update(is_checked=True)
    return redirect('index')

def reset_status(request):
    for url in UrlMonitor.objects.all():
        url.has_changed = False
        url.is_checked = False
        url.save()
    return redirect('index')
