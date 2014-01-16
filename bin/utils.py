import os
import ConfigParser

def bin_root():
    return os.path.dirname(os.path.abspath(__file__))

def project_root():
    return os.path.dirname(bin_root())

def get_config_parser():
    parser = ConfigParser.RawConfigParser()
    parser.read(os.path.join(project_root(), "year-in-review.ini"))
    return parser
    
# http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
def color(text, i):
    return "\x1b[1;%dm" % i + text + "\x1b[0m"
def red(text):
    return color(text, 31)
def green(text):
    return color(text, 32)
def yellow(text):
    return color(text, 33)
