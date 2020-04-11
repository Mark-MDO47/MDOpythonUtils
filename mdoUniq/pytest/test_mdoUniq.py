import io

from mdoUniq import *

# NOTE the file inputTest1.txt looks like this
"""
1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:DEBUG line lowercase msec 50
5:debug line lowercase MSEC 50
"""

def runCase(finp, startStr, endStr, ignore_case, goldText):
    runPass = True
    fobjOut = io.StringIO("")
    rsltNum = doMdoUniq(finp, fobjOut, startStr, endStr, ignore_case)
    rslt = fobjOut.getvalue().split("\n") # len(rslt) would have one extra ''
    while rsltNum < len(rslt):
        del rslt[-1]
    gold = goldText.split("\n")
    goldNum = len(gold)

    ign = ""
    if ignore_case:
        ign = "-i"
    cmdStr = "mdoUniq %s %s %s %s" % (ign, finp, startStr, endStr)
    fail = -1
    for idx in range(min(rsltNum, goldNum)):
        if gold[idx] != rslt[idx]:
            fail = idx
            break
    if -1 != fail:
        runPass = False
        print("FAIL (1st fail line %d): %s" % (fail+1,cmdStr))
        print("   GOLD |%s|" % gold[idx])
        print("   RSLT |%s|" % rslt[idx])
    elif rsltNum != goldNum:
        runPass = False
        print("FAIL (exp lines %d act lines %d): %s" % (goldNum, rsltNum, cmdStr))
        if rsltNum > goldNum:
            print("   1st extra RSLT |%s|" % rslt[min(rsltNum, goldNum)])
        else:
            print("   1st extra GOLD |%s|" % gold[min(rsltNum, goldNum)])
    else:
        print("PASS: %s" % cmdStr)
    return runPass

cases = [
    {"finp": "inputTest1.txt", "startStr": "a", "endStr": "b", "ignore_case": False,"goldText":
"""1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:DEBUG line lowercase msec 50
5:debug line lowercase MSEC 50"""
    },
    {"finp": "inputTest1.txt", "startStr": "a", "endStr": "b", "ignore_case": True,"goldText":
"""1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:DEBUG line lowercase msec 50"""
    },
    {"finp": "inputTest1.txt", "startStr": "D", "endStr": "m", "ignore_case": False, "goldText":
"""1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:debug line lowercase MSEC 50"""
    },
    {"finp": "inputTest1.txt", "startStr": "D", "endStr": "m", "ignore_case": True, "goldText":
"""1:DEBUG line lowercase msec 10

4:DEBUG line lowercase msec 40"""
},
    {"finp": "inputTest1.txt", "startStr": ":", "endStr": "m", "ignore_case": False, "goldText":
"""1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:debug line lowercase MSEC 50"""
     },
    {"finp": "inputTest1.txt", "startStr": "E", "endStr": "m", "ignore_case": False, "goldText":
"""1:DEBUG line lowercase msec 10
2:DEBUG line lowercase Msec 20
3:dEBUG line lowercase msec 30

4:DEBUG line lowercase msec 40
5:debug line lowercase MSEC 50"""
    }
        ]

# NOTE: the method of implementing gold text depends on \n for newline
def do_test_mdoUniq():
    numFail = 0
    for tcase in cases:
        runPass = runCase(tcase["finp"], tcase["startStr"], tcase["endStr"], tcase["ignore_case"], tcase["goldText"])
        if True != runPass:
            numFail += 1
    if 0 != numFail:
        print("Summary: FAIL %d of %d test cases" % (numFail, len(cases)))
    else:
        print("Summary: PASS all %d test cases" % len(cases))

if __name__ == "__main__":
    runPass = do_test_mdoUniq()

