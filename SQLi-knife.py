import argparse
from scripts.injection_manager import InjectionManager
import traceback

"""
Entry point of the script
imports:
-argparse -  parse terminal arguments
-scripts.injection_manager (script is folder name and injection_manager is file name) - main controller of the app to manage all subscripts
-traceback - to print detailed info about exceptions
"""


#prints meccege in nice colour box using pure python
def print_in_box(msg):
    """
    :param msg: messege to pront
    :return:
    """
    #creates top and bottom of the box
    h = ''.join(['+'] + ['-' * (len(msg) + 4)] + ['+'])
    #creates middle element of the box
    result = h + '\n'"|  " + ' '*len(msg) + "  |"'\n' + '\n'"|  " + msg + "  |"'\n' + '\n'"|  " + ' '*len(msg) + "  |"'\n' + h
    #print results and set colout back to yellow
    print('\033[0m' + result + '\033[93m')



#entry point allows to call script fro mother scripts
if __name__ == "__main__":
    try:
        #set default color to yellow
        print('\033[93m')
        #pars arguments into python variables
        argument_parser = argparse.ArgumentParser()
        # map arguments.url variable to -u parameter and set help messege (it prints when user type --help on type nothing)
        argument_parser.add_argument("-u", dest="url", help="scan website by url\nUsage: URL should have parameters, like 'http://www.mysite.org/members.php?id=1'", type=str, metavar="www.google.com")

        arguments = argument_parser.parse_args()

        #if user pass -u parameter
        if arguments.url:
            #initialize excetion manager object
            injection_manager = InjectionManager()
            #looking for vulburables (it looks like (DB, site) tuple)
            vulnerables_detected = injection_manager.scan_url(arguments.url)
            if vulnerables_detected:
                #print relust in nice black/white box
                for v in vulnerables_detected:
                    print_in_box('DB:{} Site:{}'.format(v[1], v[0]))
                #do injection. We need to cut parameters with arguments.url[:arguments.url.find("=") + 1]
                injection_manager.do_injection(arguments.url[:arguments.url.find("=") + 1])
            print('\033[0m')
        #if user pass --help ot nothing or any wronng parameter
        else:
            print('\033[0m')
            argument_parser.print_help()
            print('\033[0m')
    except Exception as e:
        #prints extended info about exception
        print "[ERR]: {}".format(e)
        print traceback.format_exc()

#NB(!) After studying this code, it is advisable to start studying the file scripts.injection_manage.py
