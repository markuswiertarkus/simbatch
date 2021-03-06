
class Logger:
    # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    console_level = 0
    log_file_level = 0
    log_file_path = ""
    force_add_to_log = False
    buffering = False
    buffer = ""

    def __init__(self, log_level=0, console_level=3):
        if console_level is None or console_level > 4:
            print "Logger init"
        self.console_level = console_level
        self.log_file_level = log_level

    def dispatch(self, level, message, force_print=False, raw=False):
        if self.console_level >= level or force_print:
            console_print = True
        else:
            console_print = False

        if self.log_file_level >= level:
            log_append = True
        else:
            log_append = False

        if level == 1:
            indent = "    "
            prefix = "INF"
        elif level == 2:
            indent = "  "
            prefix = "WRN"
        elif level == 3:
            indent = ""
            prefix = "ERR"
        elif level == 4:
            indent = "    _"
            prefix = "DB"
        elif level == 5:
            indent = "    ___"
            prefix = "deep"
        elif level == 6:
            indent = "    ___"
            prefix = "LOG"
        else:
            indent = "'"
            prefix = "_"

        if raw:
            print message
        elif console_print:
            if type(message) is tuple:
                out = "  ".join([str(el) for el in message])
                print "{}[{}] {}".format(indent, prefix, out)
            else:
                print "{}[{}] {}".format(indent, prefix, message)

        if self.force_add_to_log or log_append:
            self.add_to_log(prefix, message)

        if self.buffering is not False:
            self.buffer += "\n"+message

    def inf(self, message, force_print=False):
        self.dispatch(1, message, force_print=force_print)

    def wrn(self, message, force_print=True):
        self.dispatch(2, message, force_print=force_print)

    def err(self, message, force_print=False):
        self.dispatch(3, message, force_print=force_print)

    def db(self, message, force_print=False):
        self.dispatch(4, message, force_print=force_print)

    def deepdb(self, message, force_print=False):
        self.dispatch(5, message, force_print=force_print)

    def log(self, message, force_print=False):
        self.dispatch(6, message, force_print=force_print)
        self.add_to_log("TODO")  # TODO

    def raw(self, message):
        self.dispatch(7, message, raw=True)

    def clear_buffer(self):
        self.buffer = ""

    def get_buffer(self):
        return self.buffer

    def buffering_on(self):
        self.buffering = True

    def buffering_off(self):
        self.buffering = False

    def set_log_level(self, lvl):
        self.log_file_level = lvl

    def set_console_level(self, lvl):
        self.console_level = lvl

    def add_to_log(self, message):
        pass
        # TODO !!!
