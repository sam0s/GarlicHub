import subprocess
import json
from os import path

def dumpStats(stats):
    data = {'stats':[{'sharesfound':stats[0],
                    'sharesfailed':stats[1],
                      'hash':stats[2]}]}
    with open(path.join("currentStats.json"),'w') as outfile:
        json.dump(data, outfile, indent=4)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    
def startMine(mineFunc):
    a=execute(mineFunc)
    b=0
    sfo=0
    sfa=0
    hr=1
    for path in a:
        b+=1
        if b==5:
            b=0
            dumpStats([sfo,sfa,hr])
            print "dump"
        if "yes!" in path:sfo+=1;hr=path.split(",")[1];hr=hr[:hr.index('kH/s')+2]
        if "boo" in path:sfa+=1

startMine('dep\\ccminer-x64 --algo=scrypt:10 -o stratum+tcp://pool.grlc-bakery.fun:3333 -u GcvJyCUMgEAtLyPrEHm4qZ6avJEc674Via --max-temp=85')
