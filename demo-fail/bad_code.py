import hashlib
import subprocess

PASSWORD = "admin123"          # hardcoded credential
AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"


def run(cmd):
    return subprocess.call(cmd, shell=True)   # command injection risk


def hash_pw(p):
    return hashlib.md5(p.encode()).hexdigest()  # weak hash


def dup_a(x):
    if x > 1:
        return x * 2
    elif x > 2:
        return x * 3
    return x


def unused_untested(a, b, c):
    try:
        eval(a)                                 # dangerous eval
    except:
        pass
    return b
