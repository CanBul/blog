
from django.shortcuts import render, redirect #render is used for template bringing
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Count



class PostListView(ListView):
    model = Post
    template_name = 'blog/deneme.html' #orjinal template app/model_viewtype
    context_object_name = 'posts' #orjinal objectlist
    ordering = ['-date_posted'] #negatif ile yeniden eskiye sıralanırself.
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['konular'] = Post.objects.values_list('konu').annotate(Count('konu'))


        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['konular'] = Post.objects.values_list('konu').annotate(Count('konu'))


        return context

class SubjectView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_queryset(self):
        mylist = list(Post.objects.values_list('konu', flat=True).distinct())
        if self.kwargs['str'] in mylist:
            return Post.objects.filter(konu=self.kwargs['str']).order_by('-date_posted')
        else:
            return Post.objects.order_by('-date_posted').all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['konular'] = Post.objects.values_list('konu').annotate(Count('konu'))


        return context

def about(request):
    konular = Post.objects.values_list('konu').annotate(Count('konu'))
    return  render(request, 'blog/about.html', {'title': 'Hakkımda', 'konular':konular})


def emailView(request):
    konular = Post.objects.values_list('konu').annotate(Count('konu'))


    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['konu']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['mesaj']
            try:
                send_mail(subject, "Gondereden: "+from_email+ "\n" + "\n" + message, "contact@canbulguoglu.com", ['contact@canbulguoglu.com'])
            except BadHeaderError:
                return HttpResponse('Bilgileri kontrol ediniz.')
            messages.success(request, f'Mesajınız bana ulaşmıştır.')
            return redirect('blog-home')
    return render(request, "blog/email.html", {'form': form, 'konular':konular})
