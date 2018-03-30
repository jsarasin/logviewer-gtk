import os, io

from multiprocessing import Process, Queue, SimpleQueue
from column import MessageColumns

class SimpleParser:
    """
    This is parser module doesn't do anything fancy. It simply returns the exact string sent to it.
    """
    def __init__(self):
        pass

    def get_columns(self):
        columns = MessageColumns()
        columns.AddColumn("message", "Message", str)
        return columns

    def parse_line(self, line):
        """
        Convert a single line (tailing line return doesn't matter) into a list of values returned by get_columns()
        :param line: str: A line of text to be parsed. Training line feed not required.
        :return: [[str]]
        """
        row = {'message':line}
        return row


class ParserChooser:
    def __init__(self):
        pass

    def guess_from_sample(self, sample_messages: [str]):
        return SimpleParser()


class SyslogModule:
    class UnhandledFileChange(Exception):
        pass

    _parser_chooser = ParserChooser()

    empty = property((lambda self:self._empty), None, None, "Do any source files in this collection have data?")


    def __init__(self, service_name, service_module):
        self._service_name = service_name
        self._service_module = service_module
        self._parser_chooser = ParserChooser()
        self._parser = None
        self._sources = []
        self._historical_source = None
        self._empty = True
        self._messages = []
        self._messages_lock = False



    def get_columns(self):
        return self._parser.get_columns()


    def add_source(self, source_object):
        if os.path.islink(source_object.absolute_filename):
            return

        if source_object.file_size != 0:
            self._empty = False

        self._sources.append(source_object)

        # A parser has not been determined for this object, get one now
        if self._parser is None:
            sample_messages = ""
            self._get_older_messages_text(1000, no_decompress=True) # TODO: Multiprocess?
            self._parser = self._parser_chooser.guess_from_sample(sample_messages)

        self._historical_source = self._determine_newest_service_module_file()

    def _load_older_messages(self, try_bytes=4000, no_decompress=False):
        messages_text = self._get_older_messages_text(try_bytes, no_decompress)
        if messages_text is None:
            return None

        messages = []
        for n in messages_text:
            messages.append(self._parser.parse_line(n))

        return (self._historical_source.relative_filename, messages)

    def _determine_newest_service_module_file(self):
        lowest = None
        lowest_index = None

        for index, n in enumerate(self._sources):
            if lowest is None:
                lowest = n.roll
                lowest_index = index
                continue

            if n.roll < lowest:
                lowest = n.roll
                lowest_index = index

        if lowest_index is None:
            raise Exception("Couldn't find the most recent roll in [%s][%s]" % (self._service_name, self._service_module))

        # TODO: Check the modification date for the sanity check.
        return self._sources[lowest_index]

    def _determine_older_service_module_file(self, compare_service_module_file):
        lowest = None
        lowest_index = None

        # Find the most recent one
        if compare_service_module_file is None:
            minimum = -1
        else:
            minimum = compare_service_module_file.roll

        for index, n in enumerate(self._sources):

            if n.roll <= minimum:
                continue

            if lowest is None and n.roll > minimum:
                lowest = n.roll
                lowest_index = index
                continue

            if n.roll < lowest and n.roll > minimum:
                lowest = n.roll
                lowest_index = index

        if lowest_index is None:
            return None
            raise Exception("Couldn't find the lowest roll in [%s][%s]" % (self._service_name, self._service_module))

        # TODO: Check the modification date for the sanity check.
        return self._sources[lowest_index]


    def _update_historical_module_file(self):
        """
        When reading historical log messages, this will keep a relevant tab on which file to read through.
        """

        # Has this module been accessed at all?
        current_source = self._historical_source
        if current_source is None:
            # if self._service_name == 'samba' and self._service_module == "log.nmbd":
            #     print("accessy")

            first_service_module_file = self._determine_older_service_module_file(None)
            # if self._service_name == 'samba' and self._service_module == "log.nmbd":
            #     print("Found %s to be the oldest file" % first_service_module_file.absolute_filename)
            self._historical_source = first_service_module_file
            current_source = self._historical_source

        if current_source.read_older_position == -1:
            next_service_module_file = self._determine_older_service_module_file(current_source)

            # TODO: Notify someone that there are no more lines to be had
            if next_service_module_file is None:
                pass

            self._historical_source = next_service_module_file

    def _get_older_messages_text(self, try_bytes=4000, no_decompress=False):
        self._update_historical_module_file()
        current_file = self._historical_source
        if current_file is None:
            return None

        # The file has been exhausted
        if current_file.read_older_position == -1:
            return None

        if current_file.is_compressed:
            if no_decompress:
                return None
            else:
                raise Exception("File is compressed, cannot read: " + current_file.absolute_filename)

        if current_file.is_binary:
            return None

        fp = open(current_file.absolute_filename, 'rb')

        # First make sure the file size hasn't changed
        fp.seek(0, io.SEEK_END)
        file_size = fp.tell()
        if current_file.file_size != file_size:
            raise self.UnhandledFileChange

        start_read = current_file.read_older_position - try_bytes
        if start_read < 0:
            start_read = 0

        fp.seek(start_read)
        messages = fp.read(try_bytes-1)

        # Find the start of the first new message entry and work from there, leave the rest for the next access
        if start_read != 0:
            unused_chars = messages.find(10) + 1  #  TODO: What if -1?
        else:
            unused_chars = 0

        if unused_chars == -1:
            raise Exception("Uh oh!")

        messages = messages[unused_chars:]

        # Update our source to reflect our access
        if current_file.read_older_position - try_bytes >= 0:
            current_file._read_older_position = (current_file._read_older_position - try_bytes) + unused_chars
        else:
            current_file._read_older_position = -1

        # Convert the messages into a list and reverse it
        message_list = messages.decode('utf-8').split("\n")
        message_list.reverse()

        return message_list



