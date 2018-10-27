#!/usr/bin/env python3

import os
import glob
import random
import subprocess
import time
import datetime

DEST = "https://pi-staging.decred.org/api/"

BASECMD = ["torsocks", "python3", "sendsinglevote.py"]

MIN_SLEEPTIME = 60 # seconds
MAX_SLEEPTIME = 60 * 60 # seconds

def main():
    voteFiles = glob.glob("votes/*.vote")
    if not os.path.exists("votes/done"):
        os.mkdir("votes/done")
    if not os.path.exists("votes/receipts"):
        os.mkdir("votes/receipts")

    while len(voteFiles) > 0:
        print("%d votes left" % len(voteFiles))
        vote = random.choice(voteFiles)
        print("Going to send vote %s" % vote)
        cmd = BASECMD[:]
        cmd.extend([vote, DEST])
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        with open("votes/receipts/%s-%d.receipt" % (vote[6:-5], time.time()), "wb") as f:
            f.write(res)

        doneVote = "votes/done/"+ vote[6:]
        os.rename(vote, doneVote)

        if len(voteFiles) == 1:
            break

        sleeptime = random.randint(MIN_SLEEPTIME, MAX_SLEEPTIME)
        print("Sent vote. Gonna sleep for %s" % (datetime.timedelta(seconds=sleeptime)))
        time.sleep(sleeptime)
        voteFiles = glob.glob("votes/*.vote")

    print("Done all votes! Congrats!")




if __name__ == "__main__":
    main()
