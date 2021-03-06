#!/usr/bin/env python
#
# $NetBSD: setup.py,v 1.5 2019/01/09 19:12:14 adam Exp $
# Setup script for libxslt
#
import os
import sys
from distutils.core import setup, Extension

# Thread-enabled libxml2
with_threads = 1

# If this flag is set (windows only),
# a private copy of the dlls are included in the package.
# If this flag is not set, the libxml2 and libxslt
# dlls must be found somewhere in the PATH at runtime.
WITHDLLS = 1 and sys.platform.startswith('win')

def missing(path):
    return 1 if os.access(path, os.R_OK) == 0 else 0

HOME = os.environ.get('HOME', 'C:')

if sys.platform.startswith('win'):
    libraryPrefix = 'lib'
    platformLibs = []
else:
    libraryPrefix = ''
    platformLibs = ["m", "z"]

# those are examined to find
# - libxml2/libxml/tree.h
# - iconv.h
# - libxslt/xsltconfig.h
includes_dir = [
    "@LIBXML2DIR@/include",
    "@LIBXSLTDIR@/include"
]

xml_includes = ""
for d in includes_dir:
    if not missing(d + "/libxml2/libxml/tree.h"):
        xml_includes = d + "/libxml2"
    break

if xml_includes == "":
    sys.exit("failed to find headers for libxml2: update includes_dir")

iconv_includes = "@LIBICONVDIR@/include"

# those are added in the linker search path for libraries
libdirs = ["@LIBXML2DIR@/lib", "@PYSHLIBDIR@"]

xml_files = ["libxml2-api.xml", "libxml2-python-api.xml",
             "libxml.c", "libxml.py", "libxml_wrap.h", "types.c",
             "xmlgenerator.py", "README", "TODO", "drv_libxml2.py"]

xslt_files = ["libxslt-api.xml", "libxslt-python-api.xml",
              "libxslt.c", "libxsl.py", "libxslt_wrap.h",
              "generator.py"]

with_xslt = 0
if missing("libxslt-py.c") or missing("libxslt.py"):
    if missing("generator.py") or missing("libxslt-python-api.xml"):
        print("libxslt stub generator not found, libxslt not built")
    else:
        try:
            import generator
        except:
            print("failed to generate stubs for libxslt, aborting...")
            print(sys.exc_type, sys.exc_value)
        else:
            head = open("libxsl.py", "r")
            generated = open("libxsltclass.py", "r")
            result = open("libxslt.py", "w")
            for line in head.readlines():
                if WITHDLLS:
                    result.write(altImport(line))
                else:
                    result.write(line)
            for line in generated.readlines():
                result.write(line)
            head.close()
            generated.close()
            result.close()
            with_xslt = 1
else:
    with_xslt = 1

if with_xslt == 1:
    xslt_includes = ""
    for d in includes_dir:
        if not missing(d + "/libxslt/xsltconfig.h"):
            xslt_includes = d + "/libxslt"
            break

    if xslt_includes == "":
        print("failed to find headers for libxslt: update includes_dir")
        with_xslt = 0


descr = "libxml2 package"
modules = []
c_files = []
includes = [xml_includes, iconv_includes]
libs = ["xml2mod"] + platformLibs
macros = []
if with_threads:
    macros.append(('_REENTRANT', '1'))
if with_xslt == 1:
    descr = "libxslt package"
    if not sys.platform.startswith('win'):
        #
        # We are gonna build 2 identical shared libs with merge initializing
        # both libxml2mod and libxsltmod
        #
        c_files = c_files + ['libxslt-py.c', 'libxslt.c']
        xslt_c_files = c_files
        macros.append(('MERGED_MODULES', '1'))
    else:
        #
        # On windows the MERGED_MODULE option is not needed
        # (and does not work)
        #
        xslt_c_files = ['libxslt-py.c', 'libxslt.c', 'types.c']
    libs.insert(0, libraryPrefix + 'exslt')
    libs.insert(0, libraryPrefix + 'xslt')
    includes.append(xslt_includes)
    modules.append('libxslt')


extens = []
if with_xslt == 1:
    extens.append(Extension('libxsltmod', xslt_c_files, include_dirs=includes,
                            library_dirs=libdirs, runtime_library_dirs=libdirs,
                            libraries=libs, define_macros=macros))

if missing("MANIFEST"):
    manifest = open("MANIFEST", "w")
    manifest.write("setup.py\n")
    for file in xml_files:
        manifest.write(file + "\n")
    if with_xslt == 1:
        for file in xslt_files:
            manifest.write(file + "\n")
    manifest.close()

if WITHDLLS:
    ext_package = "libxmlmods"
    if sys.version >= "2.2":
        base = "lib/site-packages/"
    else:
        base = ""
    data_files = []
else:
    ext_package = None
    data_files = []

setup(name="libxslt-python",
      # On *nix, the version number is created from setup.py.in
      # On windows, it is set by configure.js
      version=os.environ['PYLIBXSLTVERSION'],
      description=descr,
      author="Daniel Veillard",
      author_email="veillard@redhat.com",
      url="http://xmlsoft.org/python.html",
      licence="MIT Licence",
      py_modules=modules,
      ext_modules=extens,
      ext_package=ext_package,
      data_files=data_files)
