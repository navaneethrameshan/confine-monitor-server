import pexpect
import sys
import time
import os

expectations = ['[Pp]assword',
                'continue (yes/no)?',
                pexpect.EOF,
                pexpect.TIMEOUT,
                'Name or service not known',
                'Permission denied',
                'No such file or directory',
                'No route to host',
                'Network is unreachable',
                'failure in name resolution',
                'No space left on device'
]

def scp(src, dest, child=None):
    print "Received Args:",child
    try:
        if not child:
        #child = pexpect.spawn( 'scp -r USER@SERVER.COM:%s /HOME/USER/'%(args[0]))
            child= pexpect.spawn("scp -r %s %s:." %(src, dest), timeout=150)

        res = child.expect( expectations )
        print "Child Exit Status :",child.exitstatus
        print  res,"::",child.before," :After:",child.after
        if res == 0:
            child.sendline('confine')
            return scp(None, None,child)
        if res == 1:
            child.sendline('yes')
            return scp(None, None,child)
        if res == 2:
            line = child.before
            print "Line:",line
            print "Now check the result and return status."
        if res == 3:
            print "TIMEOUT Occurred."
            child.kill(0)
            return False
        if res >= 4:
            child.kill(0)
            print "ERROR:",expectations[res]
            return False
        return True
    except:
        import traceback; traceback.print_exc()
        print "Did file finish?",child.exitstatus

if __name__ == '__main__':
    stat = True
    stat = scp('/home/navaneeth/PycharmProjects/confine_monitor/', 'root@[fdf5:5351:1dfd:37::2]')
    if stat:
        print "File Transferred successfully."
    else:
        print "Failure while copying files securely."
