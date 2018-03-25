import collections
import os
from logsystem import LogSystem, SyslogTarget
import logsystem
import time

class Catfood:
    def callback(self, event):
        if type(event) == logsystem.Event.GetServices:
            for k in event.services:
                self.services[k] = dict()

        if type(event) == logsystem.Event.GetModules:
            for m in event.modules:
                self.services[event.service_name][m[0]] = dict()

        if type(event) == logsystem.Event.GetModuleColumns:
            self.services[event.service_name][event.service_module]['columns'] = event.columns

        if type(event) == logsystem.Event.LoadOlderMessages:
            self.services[event.service_name][event.service_module]['messages'] = event.messages


    def __init__(self):
        self.services = dict()
        self.modules = None
        pass

    def go(self):
        cat = LogSystem(SyslogTarget(os.getcwd() + "/log/"), self.callback)
        result = cat.get_services()
        time.sleep(0.01)
        for n in self.services:
            result = cat.get_service_modules(n)
        time.sleep(0.01)

        cat._target.debug_printout()



        # module = cat._target._log_services['samba']['modules']['log.nmbd']
        # print("\n"*4)
        # for index, n in enumerate(module._sources):
        #     print("  %-5s:%-60s - roll: %s" % (index, n.absolute_filename, n.roll))
        # print("Historical: %s %s" % (module._historical_source.absolute_filename, module._historical_source.roll))


        # result = cat.load_older_messages("samba", "log.nmbd", 1000)
        # time.sleep (0.01)

        # print(self.services["10.0.0.2"]['boot.log']['messages'])

if __name__ == '__main__':
    cat = Catfood()
    cat.go()





    #print ("Current file: %s" % cat._log_services['alternatives.log']['modules']['alternatives.log'])


