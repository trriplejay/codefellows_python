"""
python 2.7
library.py

author: John Stockbauer
codefellows python challenge part 1

description:
This file contains the objects necessary to model a library, which includes
'Library', 'Shelf', and 'Book'

"""
# used for library objects
import functools
import bisect
from operator import attrgetter

# used for unittest
import unittest
import types



class Library(object):
	"""
	A container for shelves. Shelves contain books.

	A library contains the following attributes:
	  shelves - list of shelves in the library

	Also contains the following methods:
	  list_books - build a list of all books in the library, return a generator that produces them
	  print_books - print all books, one shelf at a time
	  checkout - remove a book from its shelf
	  book_return - put a book back on a shelf
	""" 
	def __init__(self):
		self.shelves = list()
		
	def add_shelf(self, shelf):
		# check that the shelf doesn't already exist in the library
		if shelf not in self.shelves:
			# add the new shelf
			self.shelves.append(shelf)
			
	def book_count(self):
		total = 0
		for shelf in self.shelves:
			total += len(shelf.books)
		return total

	def shelf_count(self):
		return len(self.shelves)

	def list_books(self, shelf=None):
		"""
		generates a list of all books in library, or all books from a specific shelf
		"""
		for ashelf in self.shelves:
			if shelf is not None and shelf == ashelf:
				for book in ashelf.books:
					yield book
			elif shelf is None:
				for book in ashelf.books:
					yield book

	def print_books(self, sname=None, sort_by=None):
		"""
		prints all books in the library, or prints all books
		contained by the shelf with the specified name
		sort the books in each self based on sort_by:
		  author(default)
		  title
		  isbn
		"""
		print "The library contains the following books:"
		for shelf in self.shelves:
			if sname is not None:
				if shelf.name == sname:
					print "'%s' Shelf:" % shelf.name 
					shelf.print_books(sort_by=sort_by)
			else:
				if shelf.name is not None:
					print "\n'%s' Shelf:" % shelf.name
				shelf.print_books(sort_by=sort_by)
	def checkout(self, book):
		book.unshelf()

	def book_return(self, book, shelf):
		book.enshelf(shelf)


class Shelf(object):
	"""
	A container for books.  Multiple shelves can be differentiated by giving them a name.
	A shelf contains the following attributes:
	  name - an optional argument to give the shelf a name
	  books - a list of books sitting on the shelf
	Also contains the following methods:
	  print_books - prints a formatted list of books on the shelf
	  add_book - put a book on the shelf. called by Book method "enshelf"
	  remove_book - take a book off the shelf. called by Book method "unshelf"

	"""
	def __init__(self, name=None):
		# giving a shelf a name is an optional way to add organization
		self.name = name
		# initialize the list of books that the shelf will hold
		self.books = list()

	def print_books(self, sort_by=None):
		"""
		sort books, then print them in a formatted list
		sort options are: title, author, isbn
		default sort is author->title
		"""
		if sort_by is not None:
			if sort_by.lower() == "author":
				sorted_books = sorted(self.books, key=attrgetter('author'))
			elif sort_by.lower() == "isbn":
				sorted_books = sorted(self.books, key=attrgetter('isbn'))
			else:
				# if it's not author or isbn, assume that title will be good enough
				sorted_books = sorted(self.books, key=attrgetter('title'))
			

			for book in sorted_books:
				print book
				#print("%s: \'%s\', %s" % (book.author, book.title, book.isbn))
		else:
			for book in self.books:
				print book
				#print("%s: \'%s\', %s" % (book.author, book.title, book.isbn))	


	def add_book(self, book):
		# keep books sorted by author as they are added, just like on actual library shelves
		# how to compare books is defined in the book object
		bisect.insort_left(self.books, book)

	def remove_book(self, book):
		# rather than doing a remove, which will perform linear search of the list
		# for the desired element, we'll use bisect to do a binary search, find the index
		# of the desired element, then delete it. This will save some time if our list is long.
		index = bisect.bisect_left(self.books, book)
		# make sure the book was in the list
		if(index != len(self.books) and self.books[index] == book):
			self.books.pop(index)

@functools.total_ordering
class Book(object):
	"""
	A book is an object with the following attributes:
	  author - author of the book ("lastname, firstname")
	  title - what the book is called
	  ISBN - a unique numerical identifier for the book. optional
	  shelf - a reference to the shelf that the book sits on.  A book can only be on 1 shelf at a time.
	Also contains the following methods:
	  enshelf - add a book to a shelf
	  unshelf - remove a book from its shelf
	"""
	def __init__(self, author, title, ISBN=None, shelf=None):
		self.author = author
		self.title = title
		self.isbn = ISBN
		self.shelf = shelf

	# define 2 comparison methods for books, and let functools.total_ordering do the rest
	def __eq__(self, other):
		return ((self.author.lower(), self.title.lower()) ==
			(other.author.lower(), other.title.lower()))

	def __lt__(self, other):
		return ((self.author.lower(), self.title.lower()) < 
			(other.author.lower(), other.title.lower()))

	def __str__(self):
		# define what will happen when someone calls print on a book object
		return ("%s: \'%s\', %s" % (self.author, self.title, self.isbn))

	def enshelf(self, newshelf):
		"""
		Add this book to the provided shelf.
		"""
		
		do_shelf = True

		# if already shelved, unshelf first
		if self.shelf is not None:
			if self.shelf is not newshelf:
				self.unshelf()
			else:
				# existing shelf is same as newshelf
				# no need to do anything!
				do_shelf = False

		if do_shelf:
			# enshelf the book
			self.shelf = newshelf
			newshelf.add_book(self)

	def unshelf(self):
		"""
		remove this book from the shelf it's currently on.
		"""
		if self.shelf is not None:
			self.shelf.remove_book(self)
			self.shelf = None


class TestLibrary(unittest.TestCase):
	"""
	contains unit tests for the 3 main objects that make up a library:
	  book
	  shelf
	  library
	test all functionality except for printing
	"""

	def setUp(self):
		self.library = Library()
		self.shelfA = Shelf()
		self.shelfB = Shelf()
		self.book1 = Book(author="Vonnegut, Kurt", title="Slaughterhouse 5", ISBN=12345)
		self.book2 = Book(author="Heller, Joseph", title="Catch 22", ISBN=54321)
		self.book3 = Book(author="King, Stephen", title="Gunslinger", ISBN=22333)
		self.book4 = Book(author="King, Stephen", title="The Drawing of the Three", ISBN=22334)
		self.book_list = [self.book1, self.book2, self.book3, self.book4]

	def test_book_attr(self):
		# verify attribute setup
		self.assertEqual(self.book1.author, "Vonnegut, Kurt")
		self.assertEqual(self.book2.title, "Catch 22")
		self.assertEqual(self.book3.isbn, 22333)

	def test_book_enshelf(self):
		# enshelf some books
		self.assertEqual(len(self.shelfA.books), 0)
		count = 0
		for book in self.book_list:
			book.enshelf(self.shelfA)
			count += 1
			self.assertEqual(len(self.shelfA.books), count)
		# enshelf a book on same shelf.  verify that count does not change
		self.book1.enshelf(self.shelfA)
		self.assertEqual(len(self.shelfA.books), count)

		# verify initial length of shelfB
		self.assertEqual(len(self.shelfB.books), 0)
		# enshelf a book on B that is already on A
		self.book1.enshelf(self.shelfB)
		# shelfB should have length 1 now, while shelfA is reduced by 1
		self.assertEqual(len(self.shelfB.books), 1)
		self.assertEqual(len(self.shelfA.books), count-1)

	def test_book_unshelf(self):
		self.assertEqual(len(self.shelfA.books), 0)
		count = 0
		for book in self.book_list:
			book.enshelf(self.shelfA)
			count += 1
		self.assertEqual(len(self.shelfA.books), count)
		for book in self.book_list:
			book.unshelf()
		self.assertEqual(len(self.shelfA.books), 0)
		self.assertEqual(len(self.shelfB.books), 0)

	def test_lib(self):
		self.shelfA.name = "Classics"
		self.shelfB.name = "Fantasy"
		self.book1.enshelf(self.shelfA)
		self.book2.enshelf(self.shelfA)
		self.book3.enshelf(self.shelfB)
		self.book4.enshelf(self.shelfB)
		

		self.assertEqual(self.library.shelf_count(), 0)
		
		self.library.add_shelf(self.shelfA)
		self.assertEqual(self.library.shelf_count(), 1)
		self.assertEqual(self.library.book_count(), len(self.shelfA.books))

		self.library.add_shelf(self.shelfB)
		self.assertEqual(self.library.book_count(), 4)	
		self.assertEqual(self.library.shelf_count(), 2)

		self.assertEqual(type(self.library.list_books()), types.GeneratorType)


if __name__ == '__main__':

	# uncomment to perform unittest
	# unittest does not cover methods that print to the console
	#unittest.main()
	
	# step by step exampes of all functionality described in the challenge
	library = Library()
	shelfA = Shelf()
	shelfB = Shelf()
	book1 = Book(author="Vonnegut, Kurt", title="Slaughterhouse 5", ISBN=12345)
	book2 = Book(author="Heller, Joseph", title="Catch 22", ISBN=54321)
	book3 = Book(author="King, Stephen", title="Gunslinger", ISBN=22333)
	book4 = Book(author="King, Stephen", title="The Drawing of the Three", ISBN=22334)
	book_list = [book1, book2, book3, book4]

	# perform some actions and print strings to describe whats happening
	print
	print("length of shelfA: %s" % len(shelfA.books))
	print
	print("adding 4 books to shelfA...")
	for book in book_list:
		book.enshelf(shelfA)
	print
	print("shelfA now contains:")
	shelfA.print_books()
	print
	print("remove Gunslinger from the shelf and reprint shelf:")
	book3.unshelf()
	print
	shelfA.print_books()
	print
	print("take the other King book, enshelf it to shelfB, print shelfB, then shelfA")
	print
	book4.enshelf(shelfB)
	print("shelfB contains:")
	shelfB.print_books()
	print
	print("shelfA contains:")
	shelfA.print_books()
	print
	print("enshelf Gunslinger on shelfB")
	print
	book3.enshelf(shelfB)
	print("shelfB:")
	shelfB.print_books()

	print
	print("Perform library functions...")
	print("the library currently contains *%s* shelves and *%s* books." % (library.shelf_count(), library.book_count()))
	print
	print("add shelfA to library and print library")
	library.add_shelf(shelfA)
	print("the library currently contains *%s* shelves and *%s* books." % (library.shelf_count(), library.book_count()))
	print
	library.print_books()
	print
	print("add shelfB to library and print library")
	library.add_shelf(shelfB)
	print("the library currently contains *%s* shelves and *%s* books." % (library.shelf_count(), library.book_count()))
	print
	library.print_books()
	print
	print("give names to both shelves and print library agian")
	shelfA.name = "Classic Literature"
	shelfB.name = "Fantasy"
	print
	library.print_books()
	print
	print("sort books by ISBN and print again")
	library.print_books(sort_by='isbn')
	print
	print("print the list of books that is returned from list_books method")
	print
	booklist = library.list_books()
	print("list_books should give us a generator:")
	print(booklist)
	print
	print("Iterate over the generator to print a list of books:")
	for book in booklist:
		print(book)
	print
	print("print just the books in shelfA via list_books")
	booklist = library.list_books(shelf=shelfA)
	print("the generator: " + str(booklist))
	for book in booklist:
		print(book)

