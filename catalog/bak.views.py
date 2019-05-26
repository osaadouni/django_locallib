from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Author, BookInstance, Genre, Language


# Create your views here.
#@login_required(redirect_field_name='redirect_to')
#@login_required(login_url='/login/')
@login_required()
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


class BookListView(ListView):
    model = Book
    #context_object_name = 'my_book_list' # Your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'catalog/book_list.html'
    paginate_by = 5


    def get_queryset(self):
        #return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
        return Book.objects.all().order_by('title')[:25] # Get 25 books containing the title war

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(DetailView):
    model = Author
