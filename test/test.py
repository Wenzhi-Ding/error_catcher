from error_catcher import silent
import time

@silent(key_vars=[''], log_file='', ascending=False)
def foo1():
    i, j, k = 0, 1, 2
    return k / i
foo1()

@silent(key_vars=['j'], log_file='', ascending=False)
def foo2():
    i, j, k = 0, 1, 2
    return k / i
foo2()

@silent(key_vars=['i'], log_file='', ascending=False)
def foo3():
    i, j, k = 0, 1, 2
    return k / i
foo3()

l = 4
@silent(key_vars=['l'], log_file='', ascending=False)
def foo4():
    i, j, k = 0, 1, 2
    return k / i
foo4()

@silent(key_vars=[''], log_file='test_log.log', ascending=False)
def foo5():
    i, j, k = 0, 1, 2
    return k / i
foo5()
time.sleep(3)
foo5()
time.sleep(3)

@silent(key_vars=['l'], log_file='test_log.log', ascending=True)
def foo6():
    i, j, k = 0, 1, 2
    return k / i
foo6()