from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Generate counts for genres.
    num_genres = Genre.objects.count()

    # Generate count for books that contain a particular word.
    book_filter = Book.objects.filter(
        title__contains='man').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'book_filter': book_filter,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    """BookListView class"""
    model = Book
    paginate_by = 2  # set pagination


class BookDetailView(generic.DetailView):
    """BookDetailView class"""
    model = Book


class AuthorListView(generic.ListView):
    """Author"""
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    """AuthorDetailView class"""
    model = Author


# def authors(request):
#     """author view"""
#     authors = Author.objects.all()
#     paginator = Paginator(authors, 2)  # show 5 authors per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {'page_obj': page_obj}

#     return render(request, 'catalog/author_list.html', context=context)
