#!/usr/bin/env python3
'''
Grading script for PA3 (Graphs and Networks)
Balasubramaniam Srinivasan 2018
'''
import argparse,signal
from subprocess import check_output,CalledProcessError,DEVNULL,TimeoutExpired, PIPE, Popen
from os.path import isfile
from random import sample
from time import time
import sys

# global constants
PAIRS_HEADER = "Actor1/Actress1\tActor2/Actress2"
TIME_RANGE = 2 # how many times longer student soln can take than ref soln
MIN_TIME =  15 # minimum amount of time to allow no matter how fast reference goes
LARGE_N = 15 # large number of queries
OUTPUT_P = "+8 for correct output"
OUTPUT_F = "+0 for incorrect output"
MEMLEAK_P = "+4 for no memory leaks"
MEMLEAK_F = "+0 for memory leaks"
MAX_RETRIES = 2

# definitions for killing function after certain amount of time
class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException
signal.signal(signal.SIGALRM, timeout_handler)

def year2weight(y):
    return 2018-int(y)+1

# check if given path is valid (return its weight if valid, or None if it's invalid)
def check_path(path):
    parts = path.replace('>','').split('--')
    w = 0
    for i in range(1,len(parts),2):
        m,y = parts[i][1:-1].split('#@'); a1 = parts[i-1][1:-1]; a2 = parts[i+1][1:-1]
        if a1 not in MOVIES or m not in MOVIES[a1] or y not in MOVIES[a1][m] or a2 not in MOVIES or m not in MOVIES[a2] or y not in MOVIES[a2][m]:
            return None
        w += year2weight(y)
    return w


def runCommand(command, timeout):
        proc = None
        e = None
        try:
                proc = Popen(command.split(), stdout = PIPE, stderr = PIPE)
                stdout, stderr = proc.communicate(timeout = timeout)
                return (None, proc.returncode, stdout, stderr)
        #catch all exceptions, including keyboard interrupt
        except TimeoutExpired as timeoutError:
                return (timeoutError, None, None, None)
        except:
                #I'm not sure this is necessary, but here's an attempt to handle keyboard interrupts and still kill the subprocess
                #Need to catch all exceptions so that we can catch keyboard interrupts.
                #If we don't catch a keyboard interrupt, then not even the finally block seems to run before the program dies
                #Its possible that another keyboard interrupr is sent after we enter this block before the process is killed.
                #I can't figure out any sane way to handle that
                e = sys.exc_info()[1] #stroe the error for future use
        finally:
                if proc is not None:
                        proc.kill()
                if e is not None:
                        #e wasn't an error we're expecting, so we shouldn't really have caught it,
                        #we just needed to kill the supbrocess. Now that that's done, reraise it
                        raise e



def runCommandForTest(command, timeout, possiblePoints, retryNum = 1):
        print("Command: %s" % command)

        start = time()
        timeoutError, status, stdout, stderr = runCommand(command, timeout)
        if timeoutError:
                if retryNum < MAX_RETRIES:
                        print("Your code timed out. Reattempting")
                        return runCommandForTest(command, timeout, possiblePoints, retryNum+1)
                else:
                        print("Test failed. In each of the %i tries, your program took longer than the %i seconds allocated for this test." % (MAX_RETRIES, timeout))
                        print("0/%i points awarded for this test\n" % possiblePoints)
                        return None

        end = time()
        print("Elapsed time %.10f" % (end - start))
        stdout = stdout.decode('latin-1')
        stderr = stderr.decode('latin-1')

        if status != 0:
                print("Your program crashed. 0/%i points awarded for this test" % possiblePoints)
                print("Program return value (negative values correspond to unix signals):", status)
                print("Stdout from your program command:", stdout)
                print("Stderr from your program command:", stderr)
                print("")
                return None

        return stdout



#Don't check for correct outputs, just check for memory leak
#Due to point scoring system, memLeakTest must be last
def memLeakTest(timeout):
        print("-----Running memory leak test-----")

        start = time()

        command = "valgrind --log-fd=1 --leak-check=yes ./pathfinder /home/linux/ieng6/cs100w/public/pa3/tsv/movie_casts.tsv w /home/linux/ieng6/cs100w/public/pa3/sampleInputs/sampleInputPart1 valgrindout"
        #timeout * 15 for reps, * 2 for valgrind slowdown
        output = runCommandForTest(command, timeout *5* 3 * 2, 4)
        check_output("rm -f valgrindout".split())
        if output is None:
                return False
	
        if "no leaks are possible" in output or ("definitely lost: 0 bytes" in output and
                                                "indirectly lost: 0 bytes" in output):
                print("No memory leaks detected. Memory leak test succeeded.")
                print("4/4 points awarded for the memory leak test\n")
                return True
        else:
                print("Memory leaks found. Memory leak test failed.")
                print("0/4 points awarded for the memory leak test\n")
                return False


# grade PA3
def grade(movie_casts,refpathfinder): # parameters are full paths to movie_casts.tsv file and refpathfinder and refactorconnections executables
    score = 0 # total possible = 40
    pos = 0
    actors = set()
    global MOVIES
    MOVIES = {}
    for a,t,y in [l.strip().split('\t') for l in open(movie_casts,encoding='latin-1').read().splitlines()][1:]: # ignore header line
        actors.add(a)
        if a not in MOVIES:
            MOVIES[a] = {}
        if t not in MOVIES[a]:
            MOVIES[a][t] = set()
        MOVIES[a][t].add(y)

    # check if code can compile
    print("Compiling...") #print("Checking if code compiles:")
    #pos += 1
    try:
        check_output("make clean".split())
        check_output("rm -f pathfinder".split())
        check_output("make pathfinder".split())
        if not isfile("pathfinder"):
            print("Failed to compile using 'make' command. 0 points")
            exit()
        #print("+1 for code compiling"); score += 1
    except CalledProcessError:
        print("Failed to compile using 'make' command. 0 points")
        exit()
    print()
    
    # test unweighted pathfinder
    print("Running unweighted pathfinder:")
    for _ in range(1):
        pos += 8
        pairs = [sample(actors,2) for __ in range(LARGE_N)]
        f = open('refInput','w',encoding='latin-1')
        f.write('\n'.join([PAIRS_HEADER] + ['\t'.join(p) for p in pairs]))
        f.close()
        T0 = time()
        check_output([refpathfinder,movie_casts,'u','refInput','refOutput'], stderr=DEVNULL)
        TIME = max(MIN_TIME,TIME_RANGE*int(time()-T0))
        o_ref = [l.strip() for l in open('refOutput',encoding='latin-1').read().strip().splitlines()][1:] # ignore header line
        check_output('rm -f refOutput'.split(), stderr=DEVNULL)
        try:
            signal.alarm(TIME)
            check_output(['./pathfinder',movie_casts,'u','refInput','studentOutput'], stderr=DEVNULL)
            signal.alarm(0)
            o_sol = [l.strip() for l in open('studentOutput',encoding='latin-1').read().strip().splitlines()][1:] # ignore header line
            failed = False
            if len(o_ref) == len(o_sol):
                for i in range(len(o_ref)):
                    if len(o_ref[i].split('[')) != len(o_sol[i].split('[')): # check for equal length path
                        failed = True; break
                    if check_path(o_sol[i].strip()) is None: # check if student's path is a valid path
                        failed = True; break
            else:
                failed = True
            if not failed:
                print(OUTPUT_P); score += 8
            else:
                print(OUTPUT_F)
        except CalledProcessError:
            print("Your program crashed when running the unweighted pathfinder. 0 points")
        except TimeoutException:
            print("Your program took longer than %d seconds when running the unweighted pathfinder. 0 points" % TIME)
        check_output("rm -f refInput refOutput studentOutput".split())
    print()
    
    # test large weighted pathfinder
    print("Running Weighted pathfinder:")
    for _ in range(1):
        pos += 8
        pairs = [sample(actors,2) for __ in range(LARGE_N)]
        f = open('refInput','w',encoding='latin-1')
        f.write('\n'.join([PAIRS_HEADER] + ['\t'.join(p) for p in pairs]))
        f.close()
        T0 = time()
        check_output([refpathfinder,movie_casts,'w','refInput','refOutput'], stderr=DEVNULL)
        TIME = max(MIN_TIME,TIME_RANGE*int(time()-T0))
        o_ref = [l.strip() for l in open('refOutput',encoding='latin-1').read().strip().splitlines()][1:] # ignore header line
        check_output('rm -f refOutput'.split(), stderr=DEVNULL)
        try:
            signal.alarm(TIME)
            check_output(['./pathfinder',movie_casts,'w','refInput','studentOutput'], stderr=DEVNULL)
            signal.alarm(0)
            o_sol = [l.strip() for l in open('studentOutput',encoding='latin-1').read().strip().splitlines()][1:] # ignore header line
            failed = False
            if len(o_ref) == len(o_sol):
                for i in range(len(o_ref)):
                    w_sol = check_path(o_sol[i].strip())
                    if w_sol is None or w_sol != check_path(o_ref[i].strip()): # check if student's path is a valid path
                        failed = True; break
            else:
                failed = True
            if not failed:
                print(OUTPUT_P); score += 8
            else:
                print(OUTPUT_F)
        except CalledProcessError:
            print("Your program crashed when running the weighted pathfinder. 0 points")
        except TimeoutException:
            print("Your program took longer than %d seconds when running the weighted pathfinder. 0 points" % TIME)
        check_output("rm -f refInput refOutput studentOutput".split())
    print()

    if memLeakTest(TIME):
    	score += 4
    pos+=4
    
    # clean up at the end
    print("Total Score: %d/%d" % (score,pos))
    check_output("rm -f refInput refOutput studentOutput".split())
    check_output("make clean".split())



# main function: call grader
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-mc', '--movie_casts', required=False, type=str, default="/home/linux/ieng6/cs100w/public/pa3/tsv/movie_casts.tsv", help="Full path to movie_casts.tsv file")
    parser.add_argument('-rp', '--refpathfinder', required=False, type=str, default="/home/linux/ieng6/cs100w/public/pa3/reference_binaries/refpathfinder", help="Full path to refpathfinder")
    args = parser.parse_args()
    assert isfile(args.movie_casts), "movie_casts.tsv file not found: %s" % args.movie_casts
    assert isfile(args.refpathfinder), "refpathfinder executable not found: %s" % args.refpathfinder
    grade(args.movie_casts,args.refpathfinder)

