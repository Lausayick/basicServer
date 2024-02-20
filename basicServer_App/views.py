from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def test_return(request):
    return JsonResponse({'test': '2024/2/20'})
