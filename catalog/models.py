import uuid  # Required for unique book instances
from enum import unique
from django.db import models
# Used to generate URLs by reversing the URL pattern.
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200, help_text="Enter a book genre e.g. Science Fiction")

    def __str__(self):
        """String for representing the model object."""
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief summary of the author", null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book but not a specific copy of a book."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField("ISBN", max_length=13, unique=True,
                            help_text='13 characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True)
    book_cover_image = models.ImageField(
        upload_to='book_cover_images/', null=True, default='/assets/img/book-cover2.png')
    book_content_image = models.ImageField(
        upload_to='book_content_images/', null=True, default='/assets/img/book-content.jpg')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """String for representing the book object"""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    copy_summary = models.TextField(max_length=500, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['due_back']

        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    def book_info(self):
        """Display Book id and name"""
        return f'{self.book.title} ({self.imprint})'

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""

        return bool(self.due_back and date.today() > self.due_back)
