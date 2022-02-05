import sys
import concurrent.futures

def serialize(filename, data):
    try:
        with open(filename, "a+") as f:
            f.write(data + '\n' if (data[-1] != '\n') else '')

    except Exception as e:
        print(e)
        sys.exit(1)


def deserialize(filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                yield line.rstrip()

    except Exception as e:
        print(e)
        sys.exit(1)


def thread_jobs(job, *args):
    """ Thread Functions """

    res = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # *args here unpack the tuple into single arguments
        res = executor.submit(job, *args)

    return res.result()