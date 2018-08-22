import os
import re
from datetime import datetime

class SyslogSource:
    """
    The object containing all known information *about* a log file.
    """
    _binary_check = True
    _flat_scan = False

    absolute_filename = property((lambda self: self._absolute_filename),
                                 None, None, "The full path filename")
    relative_filename = property((lambda self: self._relative_filename),
                                 None, None, "The path to the file relative to the logging root.")
    service_name = property((lambda self: self._service_name),
                            None, None, "The path to the file relative to the logging root.")
    service_module = property((lambda self: self._service_module),
                              None, None, "The path to the file relative to the logging root.")
    read_newer_position = property((lambda self: self._read_newer_position),
                                   None, None, "The location in the file we last successfully read a line from.")
    read_older_position = property((lambda self: self._read_older_position),
                                   None, None, "The location in the file we last successfully read a line from.")
    last_modified = property((lambda self: self._modified),
                             None, None, "Last modification time of this file since we read it.")
    file_size = property((lambda self: self._file_size),
                         None, None, "The last file size of this file since we read it.")
    is_binary = property((lambda self: self._is_binary),
                         None, None, "Was this file detected as being binary? This might not just indicate a"
                                     "compressed log file. For example: boot-repair will dump disk data.")
    did_binary_check = property((lambda self: self._perform_binary_check),
                                None, None, "Was binary detection performed on this file?")
    did_flat_scan = property((lambda self: self._flat_scan),
                             None, None, "Was additional information sought for when scanning this file?")
    roll = property((lambda self: self._roll),
                    None, None, "Syslog daemons will start a new file when it feels like it. The "
                                "exiting file will become .1, and it will shift older ones up numerically. This is "
                                "number.")
    is_compressed = property((lambda self: self._is_compressed),
                             None, None, "Is this file compressed?")

    _ipv4_re = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

    def _contains_non_utf8_chars(selfbytes: bytes):
        """Hack from Stackoverflow flow to detect a binary file"""
        # TODO: Does this actually check utf8??
        textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        non_utf = bool(selfbytes.translate(None, textchars))
        return non_utf

    def __init__(self, root_directory, filename, flat_scan=False, binary_check=False):
        """
        :param root_directory: The absolute path to the syslog logging folder. Eg: /var/log/
        :param filename: The absolute path to the file which to create a SyslogSource object for
        :param flat_scan: Don't try and determine file roll, service name, or service module.
        :param binary_check: Check the file for not UTF-8 Characters.
        """
        self._relative_filename = filename.replace(root_directory, '')
        self._absolute_filename = filename

        self._last_modified = os.path.getmtime(self._absolute_filename)
        self._file_size = os.path.getsize(self._absolute_filename)
        self._read_newer_position = self._file_size
        self._read_older_position = self._file_size


        if self._flat_scan:
            self._roll = None
            self._service_name = self._relative_filename
            self._service_module = self._relative_filename
        else:
            # TODO: I wonder if we couldn't pull this information out with a regex faster?
            self._get_syslog_file_information()

        self._last_modified = os.path.getmtime(self._absolute_filename)
        self._is_compressed = self._get_file_compressed()

        try:
            if self._binary_check:
                self._is_binary = SyslogSource._contains_non_utf8_chars(open(self._absolute_filename, 'rb').read(1024))
            else:
                self._is_binary = None
        except PermissionError:
            self._is_binary = None
            print("Permission Error")


    def _filename_without_path_or_compression(self) -> str:
        # Break apart any directory structure
        fwpc = self._relative_filename.rfind('/')


        # Excllude the leading / ,or if ther was none do nothing
        fwpc = self._relative_filename[fwpc + 1:]

        # Strip out file compression
        if self._relative_filename[-3:] == ".gz":
            fwpc = fwpc[0:-3]
        elif self._relative_filename[-4:] == ".bz2":
            fwpc = fwpc[0:-4]

        return fwpc

    def _filename_without_decoration(self):
        try:
            self._roll
        except:
            raise Exception("self.roll must be defined before using this")

        filename_without_decoration = self._filename_without_path_or_compression()
        if len(self._roll) > 0:
            filename_without_decoration = filename_without_decoration[0:-(len(self._roll) + 1)]

        # Detect '-YYYYMMDD' and remove it if so
        if filename_without_decoration[-9:-8] == '-':
            potential_date = filename_without_decoration[-8:]

            try:
                converted_date = datetime.strptime(potential_date, "%Y%m%d")
            except:
                converted_date = None

            if type(converted_date) is not None:
                filename_without_decoration = filename_without_decoration[0:-9]

        return filename_without_decoration

    def _detect_file_roll(self):
        # Detect Roll
        fwpc = self._filename_without_path_or_compression()

        last_period = fwpc.rfind('.')
        if last_period == -1:
            return ''
        else:
            # Does the string end with a .#?
            if fwpc[last_period+1:].isdigit():
                # Samba, and maybe other things, likes to name files by an IP address. I'm going to pretend ipv6 doesnt
                # exist.
                # TODO: Don't pretend IPv6 doesn't exist :S
                ipv4_position = self._ipv4_re.search(fwpc)

                # We found one, Let's see if there isn't a log number at the end of it
                if ipv4_position is not None:
                    ending_of_ipv4_match = fwpc[ipv4_position.end():]
                    if ending_of_ipv4_match != '':
                        return ending_of_ipv4_match[1:]
                    else:
                        return ''

                return fwpc[last_period+1:]
            else:
                return ''

    def _get_file_compressed(self):
        return self._relative_filename[-3:] == ".gz" or self._relative_filename[-4:] == ".bz2"

    def _get_syslog_file_information(self):
        slash_position = self._relative_filename.find('/')

        if slash_position != -1:
            service_name_by_enclosing_dir = True
        else:
            service_name_by_enclosing_dir = False

        self._roll = self._detect_file_roll()

        filename_without_decoration = self._filename_without_decoration()

        if not service_name_by_enclosing_dir:
            self._service_name = filename_without_decoration
            self._service_module = self._service_name

        else:
            self._service_name = self._relative_filename[0:slash_position]
            self._service_module = filename_without_decoration

        # Convert the detected roll into a number
        if self._roll == '':
            self._roll = 0
        else:
            self._roll = int(self._roll)

