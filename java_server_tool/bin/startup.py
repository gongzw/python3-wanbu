import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)





if __name__ == '__main__':
    from modules.actions import excute_from_command_line


    #excute_from_command_line(sys.argv)
    excute_from_command_line(['startup.py', 'check_status', 'all'])
    #excute_from_command_line(['startup.py', 'restart', 'service'])
