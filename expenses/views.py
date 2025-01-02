from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')

# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key()) 

# -> 34s!ff9t$he46#)qu$7re2w=8_@)&jkhrk#08r&1x54mlt(!-k
# t&y-6_b!6+29x-04vm8u(5y4vzi=*^mkfx^!hl)#jvgw0kk#t9
