from os import listdir
from os.path import isfile, join

from syslog_logger import SyslogLogger

# Terminology
# service-name
#   This is a high level service name, such as: kern, syslog, samba, apache, nginx
# service-module
#   This is a separate but related log file such as
#   Samba: /var/log/samba/log.nmbd              -   nmbd would be the service-module
#   Vmware: /var/log/vmware/hostd.log           -   hostd.log
#           /var/log/vmware/vmware-usbarb-962   -   vmware-usbarb

class Event:
    class GetServices:
        def __init__(self, services):
            self.services = services
    class GetModules:
        def __init__(self, service_name, modules):
            self.service_name = service_name
            self.modules = modules
    class GetModuleColumns:
        def __init__(self, service_name, service_module, columns):
            self.service_name = service_name
            self.service_module = service_module
            self.columns = columns
    class LoadOlderMessages:
        def __init__(self, service_name, service_module, messages):
            self.service_name = service_name
            self.service_module = service_module
            self.messages = messages


class SyslogTarget:
    def __init__(self, target_path):
        self.logger = SyslogLogger(target_path)
        self.target_path = target_path

class LogSystem:
    def __init__(self, target, callback):
        if type(target) == SyslogTarget:
            self._target_path = target.target_path
            self._target = SyslogLogger(target.target_path)
            self._client_callback = callback

            self._use_main_thread = True

    def get_services(self):
        """
        Get a list of the services detected by this LogSystem.
        :return: [str]
        """
        if self._target is not None:
            if self._use_main_thread:
                services = self._target.get_services()
                event = Event.GetServices(services)
                self._client_callback(event)

    def get_service_modules(self, service_name):
        """
        Get a list of module names.
        :return: [str]
        """
        if self._target is not None:
            if self._use_main_thread:
                modules = self._target.get_service_modules(service_name)
                event = Event.GetModules(service_name, modules)
                self._client_callback(event)

    def get_service_module_columns(self, service_name: str, service_module: str):
        """
        Get the columns dictated by the chosen parser
        :return: logsystem.MessageColumns
        """
        if self._target is not None:
            if self._use_main_thread:
                columns = self._target.get_service_module_columns(service_name, service_module)
                event = Event.GetModuleColumns(service_name, service_module, columns)
                self._client_callback(event)

    def load_older_messages(self, service_name: str, service_module: str, try_bytes: int):
        """
        Messages come in various sizes determined by a newline character. Because we cannot know
        the number of 'messages' of a given log file, or series of files, without reading the entirety
        of all related log files, we need to take guesses at how many bytes to load at one time. This
        will allow the user to specify how long they want to wait to receive the messages.

        This file does not return any values.
        :param try_bytes: Number of bytes to load and parse.
        """
        if self._target is not None:
            if self._use_main_thread:
                messages = self._target.load_older_messages(service_name, service_module, try_bytes)
                event = Event.LoadOlderMessages(service_name, service_module, messages)
                self._client_callback(event)


    def get_message_range(self, service_name: str, service_module: str, start: int, end: int):
        """
        Get a range of messages for the given module with the idicies provided.

        This library will try to make the transition between log file rolls seamless.
        This function will *hopefully* return the very last line of for example auth.log
        and the first line of auth.1.log, or auth.2.log.gz without you ever knowing.

        If there is a new entry to the log file you're reading from, and the log entry is
        being watched (see: logsystem.begin_watching), then any new entries will be accessed
        using negative numbers. For example:

        get_message_range(self, 'auth.log', 'auth.log', 0, 0)

        :param: start: The inclusive beginning of the range to collect
        :param: end: The inclusive end of the range.
        :return: [logsystem.MessageColumns]
        """
        pass

    def set_watch_callback(self, callback, user_data):
        """
        Define the method which will receive a notification when a service module has new data to be read.

        Specific service modules have to be defined to be watched using the \"begin_watching\" method.

        Arguments for callback:
        logger: The LogSystem object dispatching the event
        event: A WatchEvent object
        :param callback: The function to call on log activity, or responses to queries
        :param user_data: Any data specified by the caller. This is available to help you identify which logger
        instance you're receiving messages from.
        :return:
        """
        pass

    def begin_watching(self, service_name: str, service_module: str):
        pass

    def end_watching(self, service_name: str, service_module: str):
        pass

    def get_watching(self):
        pass

    def end_watching_all(self):
        pass
