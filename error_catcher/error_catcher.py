"""
Convenient and comprehensive traceback decorator for Python scripts.

To use this decorator, simply attach it to your function:

    from error_catcher import silent

    @silent(key_vars=[], log_file='', ascending=False)
    def func():
        i, j = 1, 0
        return i / j

    func()

Parameters
----------
key_vars ： list, default [].
    This is a list of variable names to be caught. Once an exception happens, 
    the returned message will include the corresponding value of these variables
    in the most recent frame, both globally or locally.
log_file : string, default ''.
    If this value is set non-empty, the returned message will be passed to a log 
    file under the same folder as the Python scripts. You are suggested to use 
    '.log' or '.txt' format.
    By default, it is empty and the returned message will be printed directly.
ascending : Bool, default False.
    This parameter decides whether to append the returned message to the end of
    the log file (True) or to the top of the log file (False).
    If log_file is set empty, this parameter will have no impact.
"""

import traceback
from functools import wraps
import time
import sys
import inspect
import cgitb
import linecache

__UNDEF__ = []  # To define type undefined (follow cgitb.py)


def parse_vars(vars):
    """
    Parse the returns of cgitb.scanvars to print-friendly type.
    """
    done, dump = {}, []
    for name, where, value in vars:
        if name in done: continue
        done[name] = 1
        if value is not __UNDEF__:
            dump.append(f'{where}: {name} = {value}')
        else:
            dump.append(f'{name} undefined')
    return dump


def variable_catching(key_vars):
    """
    Catch the variables that are 1) detected to be relevant to this exception and 2) manually set to be traced.
    """
    error_message = ""
    flag = 1  # Decide whether to print this section.
    context = 20  # The range to search for relevant variables (number of lines)
    records = inspect.getinnerframes(sys.exc_info()[2], context)    # Complete version in cgitb.py
    for record in records:
        frame, file, lnum = record[0], record[1], record[2]  # Complete version in cgitb.py
        locals = inspect.getargvalues(frame)[3]  # Complete version in cgitb.py

        # Detect relevant variables (copied from cgitb.py)
        highlight = {}
        def reader(lnum=[lnum]):
            highlight[lnum[0]] = 1
            try: return linecache.getline(file, lnum[0])
            finally: lnum[0] += 1
        _auto_caught_vars = cgitb.scanvars(reader, frame, locals)
        auto_caught_vars = parse_vars(_auto_caught_vars)
        done = [item[0] for item in _auto_caught_vars]  # Record variables have been caught
        
        # Catch variables that are manually set to be traced
        _manual_caught_vars = []
        for key_var in key_vars:
            if key_var not in done:
                # cgitb.lookup looks for specific variable under a frame.
                where, value = cgitb.lookup(key_var, frame, locals) 
                if where:
                    _manual_caught_vars.append((key_var, where, value))
        manual_caught_vars = parse_vars(_manual_caught_vars)

        # Assemble the contents
        if len(auto_caught_vars) + len(manual_caught_vars):
            if flag:
                error_message += "/*Variables*/\n"
                flag = 0
            error_message += f'{file}, line {lnum}\n'

        if auto_caught_vars:
            error_message += f'|-- Detected relevant vars:\n'
            for var in auto_caught_vars:
                error_message += f'  |-- {var[:200]}\n'
        
        if manual_caught_vars:
            error_message += '|-- Other traced vars:\n'
            for var in manual_caught_vars:
                error_message += f'  |-- {var[:200]}\n'
    return error_message

def silent(key_vars=[], log_file='', ascending=False):
    """
    Convenient and comprehensive traceback decorator for Python scripts.

    To use this decorator, simply attach it to your function:

        from error_catcher import silent

        @silent(key_vars=[], log_file='', ascending=False)
        def func():
            i, j = 1, 0
            return i / j

        func()

    Parameters
    ----------
    key_vars ： list, default [].
        This is a list of variable names to be caught. Once an exception happens, 
        the returned message will include the corresponding value of these variables
        in the most recent frame, both globally or locally.
    log_file : string, default ''.
        If this value is set non-empty, the returned message will be passed to a log 
        file under the same folder as the Python scripts. You are suggested to use 
        '.log' or '.txt' format.
        By default, it is empty and the returned message will be printed directly.
    ascending : Bool, default False.
        This parameter decides whether to append the returned message to the end of
        the log file (True) or to the top of the log file (False).
        If log_file is set empty, this parameter will have no impact.
    """
    def silent_decorcator(func):
        @wraps(func)
        def decorated():
            try:
                func()
            except:
                # Basic prompt
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                error_message = f'{"-" * 32}\n{timestamp}\n\n/*Original Traceback*/\n{traceback.format_exc()}\n'
                
                # Catch relevant variables
                error_message += variable_catching(key_vars)

                # Output
                if error_message: error_message += '\n\n'
                if log_file:
                    print(f'Exception caught. See {log_file}.')
                    
                    with open(log_file, 'a+') as f:
                        if ascending:
                            f.write(error_message)
                        else:
                            with open(log_file, 'r+') as f2:  # Write in this way to ensure the log file is certainly created.
                                content = f2.read()
                                f2.seek(0, 0)
                                f2.write(error_message + content)
                else:
                    print(error_message)

        return decorated
    return silent_decorcator

@silent(log_file='', key_vars=['irrelevant'], ascending=False)
def test():
    irrelevant = 123456  # To detect the catching module. This shouldn't be caught automatically but manually.
    lst = [1]
    for idx in range(2):
        print(lst[idx])

if __name__ == '__main__':
    test()