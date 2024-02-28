from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import task
from .forms import todoform
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
class tasklistview(ListView):
    model = task
    template_name = 'home.html'
    context_object_name = 'tasks'

class taskdetailview(DetailView):
    model = task
    template_name = 'detail.html'
    context_object_name = 'tasks'

class taskupdateview(UpdateView):
    model=task
    template_name = 'update.html'
    context_object_name = 'tasks'
    fields = ['name','priority','date']
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class taskdeleteview(DeleteView):
    model = task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

# Create your views here.
def index(request):
    tasks = task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        tasks=task(name=name,priority=priority,date=date)
        tasks.save()
        tasks=task.objects.all()
    return render(request,'home.html',{'tasks':tasks})
#def details(request):

   # return render(request,'detail.html',)

def delete(request,taskid):
    tasks=task.objects.get(id=taskid)
    if request.method=='POST':
        tasks.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    tasks=task.objects.get(id=id)
    forms=todoform(request.POST or None,instance=tasks)
    if forms.is_valid():
        forms.save()
        return redirect('/')
    return render(request,'edit.html',{'forms':forms,'tasks':'tasks'})
