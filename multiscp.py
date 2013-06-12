import getpass
import pexpect
import sys
import subprocess
from optparse import OptionParser

# Gobally cache password/passphrase.
_password = "confine"
_passphrase = ""

def scp(srcList, dest):
    """ 
    Copies src to dest. Initializes password/passphrase.
    """
    global _passphrase, _password
    cmd = "scp -r -o StrictHostKeyChecking=no %s %s:" % (' '.join(srcList) ,dest)
    print cmd
    tried = False
    handle = pexpect.spawn(cmd)
    index = handle.expect([".*[pP]assword:\s*", ".*[Pp]assphrase.*:\s*", pexpect.EOF, pexpect.TIMEOUT])

    while (index < 2):
        if index == 0:
            if _password == "" or tried:
                _password = getpass.getpass()
                tried = True
            handle.sendline(_password)
        elif index == 1:
            if _passphrase == "" or tried:
                _passphrase = getpass.getpass("Enter passphrase: ")
                tried = True
            handle.sendline(_passphrase)
        else:
            print handle.before
        index = handle.expect([".*[pP]assword:\s*", ".*[Pp]assphrase.*:\s*", pexpect.EOF, pexpect.TIMEOUT])

def printError(message, parser):
    parser.print_help()
    print(message)
    sys.exit(1)


def main():
    """ 
    Main function. Parses options and runs the copy.
    """
    parser = OptionParser()
    parser.add_option("-s", "--source", dest="source",
        help="source files to copy separated by , viz. foo,bar")
    parser.add_option("-t", "--target", dest="target",
        help="target nodes to copy to separated by , viz. node1,node2")
    (options, args) = parser.parse_args()
    if args:
        printError("Not expecting any argument", parser)
    if not (options.source and options.target):
        printError("Options -s and -t are required", parser)
    srcList = [src.strip() for src in options.source.split(',')]
    destList = [dest.strip() for dest in options.target.split(',')]
    for dest in destList:
        scp(srcList, dest)

if __name__ == "__main__":
    main()