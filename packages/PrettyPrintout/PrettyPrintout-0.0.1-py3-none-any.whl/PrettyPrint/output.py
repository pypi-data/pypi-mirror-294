import sys

import PrettyPrint.format as format
import time


class Printer:
    def __init__(self, log_type=None, timestamps=False):
        '''
        Initialize the Outputter. On call takes a text and prints it to console with the specified formatting
        Also logs everything to a file if log_type is {html, txt}
        :param log_type: the type of logfile created, if None, no file is created. if 'html' formatted html, if 'txt' plain text txt
        :param timestamps: controls whether to print timestamps before each output
        '''
        if log_type in ['html', 'txt']:
            self.log_type = log_type
            filename = time.strftime("%Y%m%d-%H%M")+'_PrettyPrint_Autolog'+'.'+self.log_type
            self.log = open(filename, 'w')
            if log_type == 'html':
                html_init_str = '<!DOCTYPE html>\n<html>\n  <head>\n        <title>'+filename+'</title>\n   </head>\n   <body>\n'
                self.log.write(html_init_str)
        else:
            self.log = None

        self.timestamps = timestamps

    def __call__(self, msg, fmt=None):
        '''
        Prints a formatted message to the console and logs it to a file if log_type is {html, txt}
        :param msg: String The text to be printed
        :param fmt: String The format to print with, constructed using Builder.Compose() with the ansi_util callables.
        :return:
        '''
        if isinstance(fmt, format.PPFormat):
            formatter = str(fmt)
        elif fmt is None:
            formatter = "\033[0m"
        else:
            raise ValueError(
                f"fmt is not a suppoerted datastructure, expected format.PPFormat or None, got {str(type(fmt))} instead")

        if self.timestamps:
            msg = time.strftime("%Y-%m-%d-%H:%M:%S - ")+msg

        sys.stdout.write(f"{formatter}{msg}\033[0m\n")

        if self.log is not None:
            if self.log_type == 'html':
                #self.log.write("""      <p style="color: {}; font-family: 'Liberation Sans',sans-serif">{}</p>\n""".format(colour, msg))
                self.log.write(msg + '\n')

            elif self.log_type == 'txt':
                self.log.write(msg+'\n')


    def __del__(self):
        '''
        Called on delete to close the file and finish html if log_type is html
        :return:
        '''
        if self.log is not None:
            if self.log_type == 'html':
                html_closing_str = '    </body>\n</html>'
                self.log.write(html_closing_str)
            self.log.close()


    def _tagged_print(self, msg, tag, colour):
        '''
        Prints a message with a bold and underlined tag
        :param msg: String message to print
        :param tag: String tag to print
        :param colour: String colour to print
        :return:
        '''
        colour = self._formats.fmtLookup[colour] # get colour code
        if self.timestamps: #
            tag_fmt = f"""{colour}{time.strftime("%Y-%m-%d-%H:%M:%S - ")}{self._formats.fmt_query(['bold','underline'])}{tag}{self._formats.RESET}{colour}:"""
        else:
            tag_fmt = f"{colour}{self._formats.fmt_query(['bold','underline'])}{tag}{self._formats.RESET}{colour}:"
        msg_fmt = f"{msg}{self._formats.RESET}"
        print(tag_fmt, msg_fmt)

    def warning(self, msg):
        self._tagged_print(msg, 'WARNING', 'yellow')

    def error(self, msg):
        self._tagged_print(msg, 'ERROR', 'red')

    def success(self, msg):
        self._tagged_print(msg, 'SUCCESS', 'green')

    def fail(self, msg):
        self._tagged_print(msg, 'FAIL', 'red')

