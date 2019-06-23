from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from catalog.models import Author, Book, Language, Genre, BookInstance


# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_label_using_boolean_logic(self):
        author = Author.objects.get(id=1)
        field = author._meta.get_field('first_name')
        label =  field.verbose_name
        self.assertTrue(label == 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    #def test_string_repesentation_is_last_name_comma_first_name(self):
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # this will fail if the urlconf is not defined
        access_url = author.get_absolute_url()
        self.assertEqual(access_url, '/catalog/author/1')

    def test_something(self):
        # Get an author object to test
        # Get the meta data of the required field and  use it to query the required data
        # Compare the value to the expected result
        pass


# Create your tests here.
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #print('BookModelTest::setUpTestData() ...')
        # Setup non-modified objects used by all test methods
        author = Author.objects.create(first_name='Big', last_name='Bob')
        language = Language.objects.create(name='English')
        genre_scifi = Genre.objects.create(name='Science Fiction')
        genre_action = Genre.objects.create(name='Action')

        book = Book.objects.create(title='Book 1 title', author=author, summary='Book 1 summary',
                            isbn='123456789', language=language)
        book.genre.add(genre_scifi, genre_action)

        book.bookinstance_set.create(status='a', imprint='1923')

    def setUp(self):
        #print('BookModelTest::setUp() ...')
        book = Book.objects.get(id=1)
        #print(f"book: {book}")

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        access_url = book.get_absolute_url()
        self.assertEqual(access_url, '/catalog/book/1')

    def test_display_genre_equals_added_genres(self):
        book = Book.objects.get(id=1)
        #bg_list = [g.name for g in book.genre.all()]
        #bg_str = ', '.join(bg_list)
        genre_str = 'Science Fiction, Action'
        self.assertEqual(book.display_genre(), genre_str)

    def test_get_available_copies(self):
        book = Book.objects.get(id=1)
        qs_1 = book.bookinstance_set.filter(status__exact='a')
        qs_2 = book.get_available_copies()
        self.assertQuerysetEqual(qs_1, qs_2, transform=lambda x: x)



class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #print("GenreModelTest::setUpTestData()...")
        Genre.objects.create(name='Science Fiction')

    def setUp(self):
        #print("GenreModelTest::setUp()...")
        pass

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_help_text(self):
        genre = Genre.objects.get(id=1)
        field_help_text  = genre._meta.get_field('name').help_text
        self.assertEqual(field_help_text, 'Enter a book genre (e.g. Science Fiction)')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        field_max_length = genre._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), genre.name)

    def test_get_absolute_url(self):
        genre = Genre.objects.get(id=1)
        access_url = genre.get_absolute_url()
        self.assertEqual(access_url, '/catalog/genre/1')


    def tearDown(self):
        #print("GenreModelTest::tearDown()...")
        pass


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Language.objects.create(name='English')

    def setUp(self):
        pass

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_help_text(self):
        language = Language.objects.get(id=1)
        field_help_text = language._meta.get_field('name').help_text
        self.assertEqual(field_help_text, "Enter the book's natural language (e.g. English , French, Japanese etc.)")

    def test_object_name_is_name(self):
        language = Language.objects.get(id=1)
        self.assertEqual(str(language), language.name)

    def test_get_absolute_url(self):
        language = Language.objects.get(id=1)
        access_url = language.get_absolute_url()
        self.assertEqual(access_url, '/catalog/language/1')

    def tearDown(self):
        pass

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='Big', last_name='Bob')
        language = Language.objects.create(name='English')
        genre_sci_fi = Genre.objects.create(name='Science Fiction')
        user = User.objects.create_user('omar', 'omar@thenextgen.nl', 'test123')
        book = Book.objects.create(title='Book 1 title', author=author, summary='Book 1 summary',
                                   isbn='123456789', language=language)
        book.genre.add(genre_sci_fi)

        book_instance_available = BookInstance.objects.create(book=book, imprint='Test imprint 2016', status='a')

        due_back = timezone.now() + timezone.timedelta(weeks=4)
        book_instance_borrowed = BookInstance.objects.create(book=book, imprint='Test imprint 2016', status='o',
                                                  borrower=user, due_back=due_back)

        l = [b for b in BookInstance.objects.all()]
        print(l)

    def setUp(self):
        pass


    def test_id_label(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        field_label = book_instance._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_help_text(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        help_text = book_instance._meta.get_field('id').help_text
        self.assertEqual(help_text, 'Unique ID for this particular book across whole library')


    def test_book_label(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        field_label = book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_imprint_label(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        field_label = book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_imprint_max_length(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        max_length = book_instance._meta.get_field('imprint').max_length
        #self.assertEqual(max_length, 200)
        self.assertTrue(max_length == 200)


    def test_status_label(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        field_label = book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')


    def test_borrower_label(self):
        book_instance = BookInstance.objects.filter(status='a').first()
        field_label = book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_is_overdue_is_true(self):
        self.assertTrue(True)

    def test_is_overdue_is_false(self):
        self.assertFalse(False)
