# runcommand.py
# Handy function that executes an external command in the shell
# and returns 3 values: exit code of the command, its standard output
# and its error output.
# If you run the script directly, an example is provided:
# first it will run a successful command and then one with errors
# (you may want to modify them if not running a Unix system).

import subprocess


def runcommand(cmd):
    print(f'Running {cmd}')
    print("==================================================")
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    main(proc.returncode, std_out)
    return std_out


def main(code, out):
    # code, out, err = runcommand("ls -lh");
    print("Return code: {}".format(code))
    print("--------------------------------------------------")
    print("stdout:")
    print(out)
    print("--------------------------------------------------")

    # print("==================================================")
    # print('Running "ls -lj"...')
    # print("==================================================")
    # code, out, err = runcommand("ls -lj")
    # print("Return code: {}".format(code))
    # print("--------------------------------------------------")
    # print("stdout:")
    # print(out)
    # print("--------------------------------------------------")
    # print("stderr:")
    # print(err)
    # print("--------------------------------------------------")
#
#
# if __name__ == '__main__':
#     main()