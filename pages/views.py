from django.shortcuts import render

# Create your views here.

def terms(request):
    return render(request, 'pages/terms.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

def sitemap(request):
    return render(request, 'pages/sitemap.html')