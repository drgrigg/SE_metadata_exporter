#!/usr/bin/env python3

import argparse
import os
import regex


class BookData:
	"""
	Class to hold metadata on a Standard Ebook
	"""
	title = ""
	author = ""
	pub_year = ""
	producer = ""
	translator = ""
	translated_from = ""
	translated_date = ""
	transcriber = ""
	transcription_date = ""
	cover = ""
	cover_artist = ""
	cover_year = ""
	release_date = ""
	description = ""
	long_description = ""
	language = ""
	word_count = 0
	reading_level = 0.0
	subjects = []
	sources = []
	se_link = ""

	def output_tab_delimited(self) -> str:
		"""
		Output the book data as a tab-delimited text file
		:return: one line of a tab-delimited file representing this book
		"""
		accumulator = ""
		accumulator += self.title + "\t"
		accumulator += sortable_title(self.title) + "\t"
		accumulator += self.author + "\t"
		accumulator += sortable_name(self.author) + "\t"
		accumulator += self.pub_year + "\t"
		accumulator += self.producer + "\t"
		accumulator += self.translator + "\t"
		accumulator += self.translated_from + "\t"
		accumulator += self.translated_date + "\t"
		accumulator += self.transcriber + "\t"
		accumulator += self.transcription_date + "\t"
		accumulator += self.cover + "\t"
		accumulator += sortable_title(self.cover) + "\t"
		accumulator += self.cover_artist + "\t"
		accumulator += sortable_name(self.cover_artist) + "\t"
		accumulator += self.cover_year + "\t"
		accumulator += self.release_date + "\t"
		# accumulator += self.description + "\t"
		accumulator += self.language + "\t"
		accumulator += str(self.word_count) + "\t"
		accumulator += str(self.reading_level) + "\t"
		accumulator += ",".join(self.subjects) + "\t"
		accumulator += ",".join(self.sources) + "\t"
		accumulator += 'https://standardebooks.org/ebooks/' + self.se_link
		return accumulator

	@staticmethod
	def output_headers() -> str:
		accumulator = ""
		accumulator += "Title" + "\t"
		accumulator += "Title_Sort" + "\t"
		accumulator += "Author" + "\t"
		accumulator += "Author Sort" + "\t"
		accumulator += "Year Published" + "\t"
		accumulator += "Producer" + "\t"
		accumulator += "Translator" + "\t"
		accumulator += "Translated From" + "\t"
		accumulator += "Translated Date" + "\t"
		accumulator += "Transcriber" + "\t"
		accumulator += "Transcription Year" + "\t"
		accumulator += "Cover Title" + "\t"
		accumulator += "Cover Sort" + "\t"
		accumulator += "Artist" + "\t"
		accumulator += "Artist Sort" + "\t"
		accumulator += "Cover Year" + "\t"
		accumulator += "SE Release Date" + "\t"
		# accumulator += "Description" + "\t"
		accumulator += "Language" + "\t"
		accumulator += "Word Count" + "\t"
		accumulator += "Reading Level" + "\t"
		accumulator += "Subjects" + "\t"
		accumulator += "Sources" + "\t"
		accumulator += "SE link"
		return accumulator

	def output_json(self) -> str:
		accumulator = "{" + "\n"
		accumulator += '"title" : "' + self.title + '",\n'
		accumulator += '"title_sort" : "' + sortable_title(self.title) + '",\n'
		accumulator += '"author" : "' + self.author + '",\n'
		accumulator += '"author_sort" : "' + sortable_name(self.author) + '",\n'
		accumulator += '"release_year" : "' + self.release_date[0:4] + '",\n'
		accumulator += '"release_month" : "' + self.release_date[5:7] + '",\n'
		accumulator += '"release_day" : "' + self.release_date[8:10] + '",\n'
		accumulator += '"link" : "' + 'https://standardebooks.org/ebooks/' + self.se_link + '",\n'
		accumulator += '"description" : "' + self.long_description + '",\n'
		accumulator += '"pub_year" : "' + self.pub_year + '",\n'
		accumulator += '"producer" : "' + self.producer + '",\n'
		accumulator += '"translator" : "' + self.translator + '",\n'
		accumulator += '"translated_from" : "' + self.translated_from + '",\n'
		accumulator += '"translated_date" : "' + self.translated_date + '",\n'
		accumulator += '"transcriber" : "' + self.transcriber + '",\n'
		accumulator += '"transcription_date" : "' + self.transcription_date + '",\n'
		accumulator += '"cover_title" : "' + self.cover + '",\n'
		accumulator += '"cover_sort" : "' + sortable_title(self.cover) + '",\n'
		accumulator += '"cover_artist" : "' + self.cover_artist + '",\n'
		accumulator += '"cover_artist_sort" : "' + sortable_name(self.cover_artist) + '",\n'
		accumulator += '"cover_year" : "' + self.cover_year + '",\n'
		accumulator += '"release_date" : "' + self.release_date + '",\n'
		accumulator += '"language" : "' + self.language + '",\n'
		accumulator += '"word_count" : "' + str(self.word_count) + '",\n'
		accumulator += '"reading_level" : "' + str(self.reading_level) + '"\n'

		accumulator += '}' + '\n'
		return accumulator


class TextLines:
	"""
	Helper class to locate specific information in a text file
	"""
	lines: []
	counter = 0

	def get_line_containing(self, wanted: str) -> str:
		self.counter = 0
		while self.counter < len(self.lines):
			if wanted in self.lines[self.counter]:
				return self.lines[self.counter]
			else:
				self.counter += 1
		return ""

	def get_all_containing(self, wanted: str) -> list:
		self.counter = 0
		results = []
		while self.counter < len(self.lines):
			if wanted in self.lines[self.counter]:
				results.append(self.lines[self.counter])
			self.counter += 1
		return results

	def get_next_line(self):
		self.counter += 1
		if self.counter >= len(self.lines):
			self.counter = 0
			return ""
		else:
			return self.lines[self.counter]


def month_value(month_name: str) -> str:
	"""
	Converts a string with the name of a month into its numeric equivalent
	:param month_name: string representation of the month
	:return: a string (note!) with the number of the month, left padded with zeros
	"""
	if month_name.lower() == 'january':
		return "01"
	if month_name.lower() == 'february':
		return "02"
	if month_name.lower() == 'march':
		return "03"
	if month_name.lower() == 'april':
		return "04"
	if month_name.lower() == 'may':
		return "05"
	if month_name.lower() == 'june':
		return "06"
	if month_name.lower() == 'july':
		return "07"
	if month_name.lower() == 'august':
		return "08"
	if month_name.lower() == 'september':
		return "09"
	if month_name.lower() == 'october':
		return "10"
	if month_name.lower() == 'november':
		return "11"
	if month_name.lower() == 'december':
		return "12"
	return "00"


def process_content_opf(fname: str, bd: BookData):
	"""
	Get wanted information from the content.opf file
	:param fname: path to the colophon being processed
	:param bd: instance of a book data object
	:return: qualified book data object
	"""
	opfpath = regex.sub("/text/colophon.xhtml", "/content.opf", fname)
	try:
		fileobject = open(opfpath, "r", encoding="utf-8")
	except IOError:
		print("Could not open " + opfpath)
		return
	try:
		alltext = fileobject.read()
	except UnicodeDecodeError:
		print("Could not read " + opfpath)
		return
	textlines = TextLines()
	textlines.lines = alltext.splitlines(False)
	subject_lines = textlines.get_all_containing("se:subject")
	bd.subjects = []
	for thisline in subject_lines:
		match = regex.search(r'>(.*?)<', thisline)
		if match is not None:
			bd.subjects.append(match.group(1))
	source_lines = textlines.get_all_containing("dc:source")
	bd.sources = []
	for thisline in source_lines:
		match = regex.search(r'>(.*?)<', thisline)
		if match is not None:
			bd.sources.append(match.group(1))
	thisline = textlines.get_line_containing("dc:language")
	match = regex.search(r'>(.*?)<', thisline)
	if match is not None:
		bd.language = match.group(1)
	thisline = textlines.get_line_containing("dc:description")
	match = regex.search(r'>(.*?)<', thisline)
	if match is not None:
		bd.description = match.group(1)
	thisline = textlines.get_line_containing('id="long-description"')
	accumulator = ""
	while thisline != "":
		thisline = textlines.get_next_line()
		if "</meta>" not in thisline:
			accumulator += thisline
		else:
			break
	accumulator = accumulator.replace('\t', '')
	accumulator = accumulator.replace('&lt;', '<')
	accumulator = accumulator.replace('&gt;', '>')
	# strip hyperlinks
	accumulator = regex.sub(r'<a href(?:.*?)>(.*?)</a>', '\\1', accumulator)
	# escape any remaining straight double quotes
	accumulator = accumulator.replace('"', '\\"')
	bd.long_description = accumulator
	thisline = textlines.get_line_containing("se:word-count")
	match = regex.search(r'>(\d{1,8})<', thisline)
	if match is not None:
		bd.word_count = int(match.group(1))
	thisline = textlines.get_line_containing("se:reading-ease.flesch")
	match = regex.search(r'>([0-9.]{1,8})<', thisline)
	if match is not None:
		bd.reading_level = float(match.group(1))


def process_colophon_file(fname: str) -> BookData:
	bookdata = BookData()

	try:
		fileobject = open(fname, "r", encoding="utf-8")
	except IOError:
		print("Could not open " + fname)
		return bookdata

	try:
		alltext = fileobject.read()
	except UnicodeDecodeError:
		print("Could not read " + fname)
		return bookdata

	textlines = TextLines()
	textlines.lines = alltext.splitlines(False)
	get_title_and_author(bookdata, textlines)
	get_producer(bookdata, textlines)
	get_translation(bookdata, textlines)
	get_cover_and_artist(bookdata, textlines)
	get_transcriber(bookdata, textlines)
	get_se_link(bookdata, textlines)
	get_release_date(bookdata, textlines)
	return bookdata


def get_release_date(bookdata, textlines):
	thisline = textlines.get_line_containing("The first edition of this ebook was released on")
	if thisline == "":
		thisline = textlines.get_line_containing("This edition was released on")
	if thisline != "":
		thisline = textlines.get_next_line()
		match = regex.search(r'(\w+) (\d{1,2}), (\d{4})', thisline)
		if match is not None:
			bookdata.release_date = match.group(3) + "-" + month_value(match.group(1)).zfill(2) + "-" + (match.group(2)).zfill(2)


def get_translation(bookdata, textlines):
	thisline = textlines.get_line_containing('translated from')
	if thisline != "":
		match = regex.search(r'from (.*?) (in|by)', thisline)
		if match is not None:
			bookdata.translated_from = match.group(1)
		match = regex.search(r'(\d{4})', thisline)
		if match is not None:
			bookdata.translated_date = match.group(1)
		thisline = textlines.get_next_line()
		match = regex.search(r'>(.*?)<', thisline)
		if match is not None:
			bookdata.translator = match.group(1)
		bookdata.translator = remove_class_name(bookdata.translator)


def get_se_link(bookdata, textlines):
	thisline = textlines.get_line_containing("standardebooks.org/ebooks/")
	if textlines != "":
		match = regex.search(r'>standardebooks.org/ebooks/(.*?)<', thisline)
		if match is not None:
			bookdata.se_link = match.group(1)


def get_transcriber(bookdata, textlines):
	thisline = textlines.get_line_containing("a transcription")
	if thisline != "":
		match = regex.search(r'in (\d{4})', thisline)
		if match is not None:
			bookdata.transcription_date = match.group(1)
		thisline = textlines.get_next_line()
		# this is VERY MESSY, transcriber line is not very well standardised
		match_list = regex.findall(r'<(?:a|b) class="name">(.*?)</(?:a|b)>', thisline)
		for name in match_list:
			bookdata.transcriber += name + ", "
		bookdata.transcriber = bookdata.transcriber[:-2]
		if "Proofreading" in thisline:
			if bookdata.transcriber != "":
				bookdata.transcriber += ", The Online Distributed Proofreading Team"
			else:
				bookdata.transcriber += "The Online Distributed Proofreading Team"
		bookdata.transcriber = remove_abbr(bookdata.transcriber)


def get_cover_and_artist(bookdata, textlines):
	thisline = textlines.get_line_containing("The cover page")
	if thisline != "":
		thisline = textlines.get_next_line()
		match = regex.search(r'>(.*?)</i>', thisline)
		if match is not None:
			bookdata.cover = match.group(1)
		else:
			match = regex.search(r'>, (.*?)[\.,]', thisline)
			if match is not None:
				bookdata.producer = match.group(1)
		bookdata.cover = remove_abbr(bookdata.cover)
		thisline = textlines.get_next_line()
		match = regex.search(r'completed (in|around|about) (\d{4})', thisline)
		if match is not None:
			bookdata.cover_year = match.group(2)
		thisline = textlines.get_next_line()
		# artist line may or may not be hyperlinked
		match = regex.search(r'>(.*?)</a>', thisline)
		if match is not None:
			bookdata.cover_artist = match.group(1)
		else:
			match = regex.search(r'^\t{0,4}(.*?)\.<br/>', thisline)
			if match is not None:
				bookdata.cover_artist = match.group(1)
		bookdata.cover_artist = remove_abbr(bookdata.cover_artist)


def get_producer(bookdata, textlines):
	thisline = textlines.get_line_containing("Standard Ebooks project")
	if thisline != "":
		textlines.get_next_line()  # should be "by"
		thisline = textlines.get_next_line()
		# author line may or may not be hyperlinked
		match = regex.search(r'>(.*?)</a>', thisline)
		if match is not None:
			bookdata.producer = match.group(1)
		else:
			match = regex.search(r'^\t{0,4}(.*?)[\.,]', thisline)
			if match is not None:
				bookdata.producer = match.group(1)
		bookdata.producer = remove_class_name(bookdata.producer)


def get_title_and_author(bookdata, textlines):
	thisline = textlines.get_line_containing("se:name.publication")
	if thisline != "":
		match = regex.search(r'<i(.*?)">(.*?)</i>', thisline)
		if match is not None:
			bookdata.title = match.group(2)
		bookdata.title = remove_abbr(bookdata.title)
		thisline = textlines.get_next_line()
		match = regex.search(r'(published|written|compiled) (in|between|around) (.*?) by', thisline)
		if match is not None:
			bookdata.pub_year = match.group(3)
		# remove era
		if '<abbr class="era">' in bookdata.pub_year:
			bookdata.pub_year = regex.sub(r'<abbr class="era">BC</abbr>', 'BC', bookdata.pub_year)
			bookdata.pub_year = regex.sub(r'<abbr class="era">AD</abbr>', 'AD', bookdata.pub_year)
		thisline = textlines.get_next_line()
		# author line may or may not be hyperlinked
		match = regex.search(r'>(.*?)</a>', thisline)
		if match is not None:
			bookdata.author = match.group(1)
		else:
			match = regex.search(r'^\t{0,4}(.*?)\.', thisline)
			if match is not None:
				bookdata.author = match.group(1)
		# may need to clean up abbreviations in name
		bookdata.author = remove_abbr(bookdata.author)


def sortable_name(string_value: str) -> str:
	# assumes last word in string is the surname
	names = string_value.split(" ")
	if len(names) > 1:
		accumulator = names[len(names) - 1]
		accumulator += ", "
		for i in range(0, len(names) - 1):
			accumulator += names[i] + " "
		string_value = accumulator
	return string_value


def sortable_title(string_value: str) -> str:
	match = regex.search(r'(A|An|The) (.*?)$', string_value)
	if match is not None:
		string_value = match.group(2) + ", " + match.group(1)
	return string_value


def remove_class_name(string_value: str) -> str:
	if '<abbr' in string_value:
		string_value = regex.sub(r'<abbr class="name">', '', string_value)
		string_value = regex.sub(r'</abbr>', '', string_value)
	if '<b class="name">' in string_value:
		string_value = regex.sub(r'<b class="name">', '', string_value)
		string_value = regex.sub(r'</b>', '', string_value)
	return string_value


def remove_abbr(string_value: str) -> str:
	if '<' in string_value:
		string_value = regex.sub(r'<abbr.*?>', '', string_value)
		string_value = regex.sub(r'</abbr>', '', string_value)
		string_value = regex.sub(r'<i.*?>', '', string_value)
		string_value = regex.sub(r'</i>', '', string_value)
		string_value = regex.sub(' ', ' ', string_value)
	return string_value


def main():
	parser = argparse.ArgumentParser(description="Read colophon and content.opf and output useful metadata.")
	parser.add_argument("directory", metavar="DIRECTORY", help="top-level directory to search")
	parser.add_argument("-t", "--tab", action="store_true", help="output tab delimited text, not JSON")
	args = parser.parse_args()

	colophon_list = []

	for root, d_names, f_names in os.walk(args.directory):
		for f_name in f_names:
			if "colophon.xhtml" in f_name:
				colophon_list.append(os.path.join(root, f_name))
	book_list = []

	if args.tab:
		print(BookData.output_headers())
	for cfile in colophon_list:
		if not os.path.exists(cfile):
			print("Error: this file does not exist: " + cfile)
			exit(-1)
		elif not os.path.isfile(cfile):
			print("Error: this is not a file")
			exit(-1)
		bd = process_colophon_file(cfile)
		process_content_opf(cfile, bd)
		book_list.append(bd)

	for book in book_list:
		if args.tab:
			print(book.output_tab_delimited())
		else:
			print(book.output_json())


if __name__ == "__main__":
	main()
