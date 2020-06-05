import datetime
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect

from .models import Book,BookInstance, Author, Genre
from .forms import RenewBookForm,RenewBookModelForm


def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_visits': num_visits
        }
    )

class BookListView(generic.ListView):
    # 页面默认的变量是book_list(model_name_list)或object_list
    model = Book
    template_name = 'book_list.html'
    paginate_by = 2
    queryset = Book.objects.all()

class BookDetailView(generic.DetailView):
    # 页面默认的变量是book(model_name)或object
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    # 默认中跳转至catalog/author_list.html
    # template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    modal = Author
    # 默认跳转
    # template_name = 'author_detail.html'
    def get_queryset(self):
        return Author.objects.filter(pk__exact = self.kwargs.get('pk'))

@method_decorator(login_required, name='dispatch')
class LoanedBooksByUserListView(generic.ListView):
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(
                borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# @method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_mark_returned'), name='dispatch')
class LoanedBooksByAllListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['all_book_list'] = True
        return context
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)
        # Check if the form is valid:
        if form.is_valid(): 
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date,})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


# 创建和更新需要指定显示的fields 它们使用相同的模版 名称为
# 增加template_name_suffix属性更改默认文件的后缀名
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_mark_returned'), name='dispatch')
class AuthorCreate(generic.CreateView):
    model = Author
    fields = '__all__'
    # 默认文件路径 author_form.html(modelName_form.html)
    # template_name = 'catalog/author_form.html'
    initial={'date_of_death':'2018-01-01',}


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_mark_returned'), name='dispatch')
class AuthorUpdate(generic.UpdateView):
    model = Author
    # 增加指定要修改的字段
    fields = ['first_name','last_name','date_of_birth','date_of_death']



@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_mark_returned'), name='dispatch')
class AuthorDelete(generic.DeleteView):
    model = Author
    # 默认的删除页面路径 modelName_confirm_delete.html
    # template_name = 'catalog/author_confirm_delete.html'
    # 删除需要指定删除成功后跳转的url
    success_url = reverse_lazy('authors')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('catalog.can_mark_returned'), name='dispatch')
class BookAdd(generic.CreateView):
    model = Book
    fields = '__all__'