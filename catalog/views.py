import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.models import Group, Permission
from django.core import paginator


from .models import Book, Author, BookInstance, Genre, Language
from .forms import RenewBookForm, RenewBookModelForm, BookModelForm, BookInstanceModelForm, BorrowBookInstanceModelForm


# Create your views here.
def email_check(user):
    #return user.email.endswith('@example.com')
    return True


#@login_required(redirect_field_name='redirect_to')
#@login_required(login_url='/login/')
@login_required()
@user_passes_test(email_check)
def index(request):
    """View function for home page of site."""

    if request.session.test_cookie_worked():
        print('Session worked!')
        #request.session.delete_test_cookie()
        #return HttpResponse('session worked!')
    else:
        print("request.session.set_test_cookie()")
        #request.session.set_test_cookie()


    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres_fiction = Genre.objects.filter(name__icontains='fiction').distinct().count()
    num_books_fiction = Book.objects.filter(genre__name__icontains='fiction').distinct().count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    #request.session.set_expiry(300)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_fiction': num_genres_fiction,
        'num_books_fiction': num_books_fiction,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


class BookListView(LoginRequiredMixin,
                   #UserPassesTestMixin,
                   ListView):
    model = Book
    #context_object_name = 'my_book_list' # Your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'catalog/book_list.html'
    paginate_by = 5

    raise_exception = True
    permission_denied_message = "Hush hush !! "

    #login_url = '/login/'
    #login_url = reverse('login')
    #redirect_field_name = 'redirect_to'

    def test_func(self):
        print("BookListView::test_func()")
        #return self.request.user.email.endswith('@amstelnet.com')
        return True

    def get_queryset(self):
        print("BookListView::get_queryset()")
        #return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
        return Book.objects.all().order_by('title')[:25] # Get 25 books containing the title war

    def get_template_names(self):
        print('BookListView::get_template_names()')
        return [self.template_name]

    def dispatch(self, *args, **kwargs):
        print('BookListView::dispatch()')
        print(f"BookListView::self.request.user: {self.request.user}")
        print(f"BookListView::self.template_name: {self.template_name}")

        #if self.request.user.groups.filter(name__icontains='librarian').exists():
        #    self.template_name = 'catalog/book_list_librarian.html'
        print(f"BookListView::self.template_name: {self.template_name}")

        print(f"BookListView::self.request.user: {self.request.user}")
        if self.request.user.is_authenticated:
            self.user_permissions = list(Permission.objects.filter(group__user=self.request.user).values_list('codename', flat=True))
        else:
            self.user_permissions = []

        print(self.user_permissions)

        return super().dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        print("BookListView::get()")
        print(f"BookListView::request.user: {request.user}")
        print(f"BookListView::self.template_name: {self.template_name}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print("BookListView::get_context_data()")
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['user_permissions'] = self.user_permissions
        return context


class BookDetailView(LoginRequiredMixin,
                     DetailView):
    model = Book
    bookinstances_paginate_by = 5

    def dispatch(self, *args, **kwargs):
        print('dispatch()')
        self.object = self.get_object()
        print(f'self.object: {self.object}')
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['book'] = self.object
        context_data['action'] = 'Add'

        # paginate related objects  - param: ?ro_page=<x>
        ro_page = self.request.GET.get('ro_page')
        bookinstances = self.object.bookinstance_set.all()
        bookinstances_paginator = paginator.Paginator(bookinstances, self.bookinstances_paginate_by)

        # Catch invalid page numbers
        try:
            bookinstances_page_obj = bookinstances_paginator.page(ro_page)
        except (paginator.PageNotAnInteger, paginator.EmptyPage):
            bookinstances_page_obj = bookinstances_paginator.page(1)

        print(f"bookinstances_page_obj: {bookinstances_page_obj}")
        print(f"bookinstances_page_obj.has_other_pages: {bookinstances_page_obj.has_other_pages()}")
        print(f"bookinstances_paginator.num_pages: {bookinstances_paginator.num_pages}")

        context_data['related_page_obj'] = bookinstances_page_obj

        return context_data


class BookCreateView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookCreateView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['action'] = 'New'
        return context


class BookUpdateView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['action'] = 'Update'
        return context


class BookDeleteView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


class BookReturnView(LoginRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['due_back', 'status']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        request.POST['due_back'] = None
        request.POST['status'] = 'a'
        return super(BookReturnView, self).post(request, **kwargs)

    def get(self, request, **kwargs):
        self.object = self.get_object()
        print("object:")
        print(self.object)
        print(f"id: {self.object.id}")
        print(f"due_back: {self.object.due_back}")
        print(f"status: {self.object.status}")
        print(f"path: {self.request.path_info}")
        prev_page = request.META.get('HTTP_REFERER', '/')
        print(f"prev_page: {prev_page}")
        obj = self.object
        obj.due_back = None
        obj.status = 'a'
        obj.save()
        return HttpResponseRedirect(prev_page)


#class AuthorListView(LoginRequiredMixin, ListView):
class AuthorListView(ListView):
    model = Author
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        #print('AuthorListView::dispatch()')
        #print(f"AuthorListView::dispatch(): self.request.user: {self.request.user}")

        if self.request.user.is_authenticated:
            self.user_permissions = list(Permission.objects.filter(group__user=self.request.user).values_list('codename', flat=True))
        else:
            self.user_permissions = []
        #print(f"AuthorListView::dispatch() - self.user_permissions: {self.user_permissions}")
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data and add it to the context
        context['user_permissions'] = self.user_permissions
        return context


class AuthorDetailView(LoginRequiredMixin,
                       DetailView):
    model = Author

    def dispatch(self, *args, **kwargs):
        print('AuthorListView::dispatch()')
        print(f"AuthorListView::self.request.user: {self.request.user}")
        if self.request.user.is_authenticated:
            self.user_permissions = list(Permission.objects.filter(group__user=self.request.user).values_list('codename', flat=True))
        else:
            self.user_permissions = []

        print(self.user_permissions)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data and add it to the context
        context['user_permissions'] = self.user_permissions
        return context


class LoanedBooksByUserListView(LoginRequiredMixin,
                                ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LibrarianListView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        ListView):
    """Generic class-based view specific to librarians listing borrowed books."""

    model = BookInstance
    template_name = 'catalog/librarian_page.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required()
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form Data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL
            return HttpResponseRedirect(reverse('librarian-view'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_form.html', context)




# CBVS
class AuthorCreate(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   CreateView):
    model = Author
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}
    #template_name = 'catalog/author_create_form.html'
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class WorksAuthorBookAddView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        View):
    # model = Book
    #fields = '__all__'
    form_class = BookModelForm
    fields = ['title', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/author_book_add_form.html'

    #def get_queryset(self):
    #    books = Book.objects.none()
    #    return books

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print('get()')

        context = {'form': form, 'author': self.author } # self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('post()')
        form = self.form_class(request.POST)

        if form.is_valid():
            print('form is valid')
            book = form.save(commit=False)
            book.author = self.author
            book.save()
            print(f"book.id: {book.id}")
            print("redirect to author-detail")
            return HttpResponseRedirect(reverse('author-detail', args=[str(self.author.pk)]))

        context = {'form': form, 'author': self.author } # self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, context)



    def dispatch(self, *args, **kwargs):
        print('dispatch()')
        self.author = get_object_or_404(Author, pk=kwargs['pk'])
        print(f"self.author: {self.author}")
        #self.object = self.get_object()

        return super(AuthorBookAddView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
         context_data = super(AuthorBookAddView, self).get_context_data(*args, **kwargs)
         context_data['author'] = self.author
         #self.object = self.get_object()
         #self.object.author = self.author
         context_data['action'] = 'Add'
         return context_data

    def form_valid(self, form):
        form.instance.author = self.author
        return super().form_valid(form)

        #book = form.save(commit=False)
        #book.author = self.author#
        #book.save()
        #response = super(AuthorBookAddView, self).form_valid(form)

        # Do something with self.object
        #return response



class AuthorBookAddView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        CreateView):

    form_class = BookModelForm
    #permission_required = 'catalog.can_mark_returned'
    permission_required = 'catalog.add_book'
    template_name = 'catalog/author_book_add_form.html'

    def dispatch(self, *args, **kwargs):
        print('dispatch()')
        self.author = get_object_or_404(Author, pk=kwargs['pk'])
        print(f"self.author: {self.author}")
        return super(AuthorBookAddView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(AuthorBookAddView, self).get_context_data(*args, **kwargs)
        context_data['author'] = self.author
        context_data['action'] = 'Add'
        return context_data

    def form_valid(self, form):
        form.instance.author = self.author
        return super().form_valid(form)


class  BookCopyAddView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        CreateView):

    form_class = BookInstanceModelForm
    permission_required = 'catalog.add_book'
    template_name = 'catalog/book_copy_add_form.html'


    def dispatch(self, *args, **kwargs):
        print('dispatch()')
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        print(f"self.book: {self.book}")
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['book'] = self.book
        context_data['action'] = 'Add'
        return context_data

    def form_valid(self, form):
        form.instance.book = self.book
        return super().form_valid(form)

    def get_success_url(self,  **kwargs):
        return reverse_lazy('book-detail', args=[str(self.book.pk)])



class  BookCopyBorrowView(LoginRequiredMixin,
                       #PermissionRequiredMixin,
                       UpdateView):

    model = BookInstance
    form_class = BorrowBookInstanceModelForm
    #permission_required = 'catalog.add_book'
    template_name = 'catalog/book_copy_borrow_form.html'


    def get(self, request, *args, **kwargs):
        print("BookCopyBorrowView()::get()")
        #:w
        #:self.object = None # self.get_object()
        due_back_date = datetime.date.today() + datetime.timedelta(weeks=3)
        print(f"due_back_date: {due_back_date}")
        print(f"self.object.id: {self.object.id}")
        form = BorrowBookInstanceModelForm(initial={'id': self.object.id, 'due_back': due_back_date, 'book': self.book, 'isbn': self.book.isbn})

        context = self.get_context_data(*args, **kwargs) # {'form': form}
        context['form'] = form
        print(context)
        return render(request, self.template_name, context)

    def dispatch(self, *args, **kwargs):
        print("BookCopyBorrowView()::dispatch()")
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        self.object = get_object_or_404(BookInstance, pk=kwargs['id'])
        self.object_id = kwargs['id']

        print(f"[BookCopyBorrowView()::self.book: {self.book}")
        print(f"[BookCopyBorrowView()::self.object: {self.object}")

        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("BookCopyBorrowView()::post()")
        self.object = self.get_object()
        print(f"BookCopyBorrowView()::post():self.object: {self.object}")
        return super().post(request, *args, **kwargs)

    def get_object(self):
        print("BookCopyBorrowView()::get_object()")
        print(f"BookCopyBorrowView()::self.object_id: {self.object_id}")
        return self.object # BookInstance.objects.get(pk=self.object_id)  # or request.POST

    def get_context_data(self, *args, **kwargs):
        print("BookCopyBorrowView()::get_context_data()")
        context_data = super().get_context_data(*args, **kwargs)
        context_data['book'] = self.book
        context_data['action'] = 'Borrow'

        return context_data

    def form_valid(self, form):
        print("BookCopyBorrowView()::form_valid()")
        form.instance.book = self.book
        form.instance.borrower = self.request.user
        form.instance.status = 'o'

        print(f"form.instance.id: {form.instance.id}")
        print(f"form.instance.book: {form.instance.book}")
        print(f"form.instance.borrower: {form.instance.borrower}")
        print(f"form.instance.due_back: {form.instance.due_back}")
        print(f"form.instance.status: {form.instance.status}")
        return super().form_valid(form)

    def get_success_url(self,  **kwargs):
        return reverse_lazy('book-detail', args=[str(self.book.pk)])



# Genre Class
class GenreDetailView(LoginRequiredMixin,
                     DetailView):
    model = Genre


# Language Class
class LanguageDetailView(LoginRequiredMixin,
                         DetailView):
    model = Language
