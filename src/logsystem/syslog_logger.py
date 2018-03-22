import io
import os
import mimetypes

from syslog_source import SyslogSource
from syslog_module import SyslogModule
import column


class SyslogLogger:
    _data_path = str
    _log_services = []

    def __init__(self, service_path):
        super().__init__()
        self._optimize = False

        self._data_path = service_path
        self._log_services = dict()

        self._scan_service_path(service_path)

    def get_services(self):
        """ Get a list of the services detected by this LogSystem
            Returns: [str]
        """
        services = []
        for n in sorted(self._log_services):
            services.append(n)

        return services

    def get_service_modules(self, service_name):
        """
        Return a list of module names, empty
        :return: [str, bool]
        """
        if service_name not in self._log_services:
            raise Exception("Cat food doesnt taste good.")

        modules = []
        for n in sorted(self._log_services[service_name]['modules']):
            empty = self._log_services[service_name]['modules'][n].empty

            modules.append([n, empty])

        return modules

    def get_service_module_sources(self, service_name, service_module):
        """ Get a list of the specified modules sources.

            Returns: [SyslogSource]
        """
        module = self._log_services[service_name]['modules']
        pass

    def get_service_module_columns(self, service_name, service_module):
        columns = self._get_module_class(service_name, service_module).get_columns();

        return columns

    def load_older_messages(self, service_name: str, service_module: str, try_bytes: int):
        module = self._get_module_class(service_name, service_module)
        messages = module._load_older_messages(try_bytes)

        return messages

    def get_message_range(self, service_name, service_module, start, end):
        pass

    def _get_module_class(self, service_name, service_module):
        """
        Return an existing or new SyslogModule at the specified path
        :return: SyslogModule
        """
        if service_name not in self._log_services:
            self._log_services[service_name] = dict()
            self._log_services[service_name]['modules'] = dict()

        if service_module not in self._log_services[service_name]['modules']:
            self._log_services[service_name]['modules'][service_module] = \
                SyslogModule(service_name, service_module)

        return self._log_services[service_name]['modules'][service_module]


    def _add_log_source_entry(self, full_filename, syslog_source_object):
        # Ignore links
        if os.path.islink(full_filename) is True:
            return
        module_class = self._get_module_class(syslog_source_object.service_name, syslog_source_object.service_module)

        module_class.add_source(syslog_source_object)

    def _scan_service_path(self, service_path):
        def walk_error(onerror):
            raise IOError

        for root, dirs, files in os.walk(self._data_path, onerror=walk_error):
            if root != self._data_path:
                root = root + "/"

            for filename in files:
                full_filename = root + filename

                # File is a link
                if os.path.islink(full_filename) is True:
                    continue

                # File is empty
                if self._optimize and os.path.getsize(full_filename) == 0:
                    continue

                syslog_source = SyslogSource(self._data_path, full_filename)

                if syslog_source is not None:
                    self._add_log_source_entry(full_filename, syslog_source)

