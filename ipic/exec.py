import subprocess, threading, sys

stdout_result = 1
stderr_result = 1

def stdout_thread(pipe, func):
    global stdout_result
    while True:
        out = pipe.stdout.read(1)
        stdout_result = pipe.poll()
        if out == '' and stdout_result is not None:
            break

        if out != '':
            func(out.decode("utf-8"))


def stderr_thread(pipe, func):
    global stderr_result
    while True:
        err = pipe.stderr.read(1)
        stderr_result = pipe.poll()
        if err == '' and stderr_result is not None:
            break

        if err != '':
           func(err.decode("utf-8"))


def exec_command(command, iout_func=lambda x: print(x, end=""), bout_func=print, err_func=lambda x: print(x, end=""), cwd=None):
    if cwd is not None:
        bout_func('[' + ' '.join(command) + '] in ' + cwd)
    else:
        bout_func('[' + ' '.join(command) + ']')

    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )

    out_thread = threading.Thread(name='stdout_thread', target=stdout_thread, args=(p, iout_func))
    err_thread = threading.Thread(name='stderr_thread', target=stderr_thread, args=(p, err_func))

    err_thread.start()
    out_thread.start()