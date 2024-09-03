"""
modulegraph.find_modules - High-level module dependency finding interface
=========================================================================

History
........

Originally (loosely) based on code in py2exe's build_exe.py by Thomas Heller.
"""
from __future__ import absolute_import 

import os 
import sys 
import warnings 

from .import _imp as imp 
from .import modulegraph 
from .modulegraph import Alias ,Extension ,Script 
from .util import imp_find_module 

__all__ =["find_modules","parse_mf_results"]

_PLATFORM_MODULES ={"posix","nt","os2","mac","ce","riscos"}


def get_implies ():
    result ={


    "_curses":["curses"],
    "posix":["resource"],
    "gc":["time"],
    "time":["_strptime"],
    "datetime":["time"],
    "MacOS":["macresource"],
    "cPickle":["copy_reg","cStringIO"],
    "parser":["copy_reg"],
    "codecs":["encodings"],
    "cStringIO":["copy_reg"],
    "_sre":["copy","string","sre"],
    "zipimport":["zlib"],

    "_datetime":["time","_strptime"],
    "_json":["json.decoder"],
    "_pickle":["codecs","copyreg","_compat_pickle"],
    "_posixsubprocess":["gc"],
    "_ssl":["socket"],

    "_elementtree":["copy","xml.etree.ElementPath"],




    "anydbm":["dbhash","gdbm","dbm","dumbdbm","whichdb"],

    "wxPython.wx":Alias ("wx"),
    }

    if sys .version_info [0 ]==3 :
        result ["_sre"]=["copy","re"]
        result ["parser"]=["copyreg"]


        result ["_frozen_importlib"]=None 

    if sys .version_info [0 ]==2 and sys .version_info [1 ]>=5 :
        result .update (
        {
        "email.base64MIME":Alias ("email.base64mime"),
        "email.Charset":Alias ("email.charset"),
        "email.Encoders":Alias ("email.encoders"),
        "email.Errors":Alias ("email.errors"),
        "email.Feedparser":Alias ("email.feedParser"),
        "email.Generator":Alias ("email.generator"),
        "email.Header":Alias ("email.header"),
        "email.Iterators":Alias ("email.iterators"),
        "email.Message":Alias ("email.message"),
        "email.Parser":Alias ("email.parser"),
        "email.quopriMIME":Alias ("email.quoprimime"),
        "email.Utils":Alias ("email.utils"),
        "email.MIMEAudio":Alias ("email.mime.audio"),
        "email.MIMEBase":Alias ("email.mime.base"),
        "email.MIMEImage":Alias ("email.mime.image"),
        "email.MIMEMessage":Alias ("email.mime.message"),
        "email.MIMEMultipart":Alias ("email.mime.multipart"),
        "email.MIMENonMultipart":Alias ("email.mime.nonmultipart"),
        "email.MIMEText":Alias ("email.mime.text"),
        }
        )

    if sys .version_info [:2 ]>=(2 ,5 ):
        result ["_elementtree"]=["pyexpat"]

        import xml .etree 

        files =os .listdir (xml .etree .__path__ [0 ])
        for fn in files :
            if fn .endswith (".py")and fn !="__init__.py":
                result ["_elementtree"].append ("xml.etree.%s"%(fn [:-3 ],))

    if sys .version_info [:2 ]>=(2 ,6 ):
        result ["future_builtins"]=["itertools"]



    result ["os.path"]=Alias (os .path .__name__ )

    return result 


def parse_mf_results (mf ):
    """
    Return two lists: the first one contains the python files in the graph,
    the second the C extensions.

    :param mf: a :class:`modulegraph.modulegraph.ModuleGraph` instance
    """

    py_files =[]
    extensions =[]

    for item in mf .flatten ():


        if item .identifier =="__main__":
            continue 
        src =item .filename 
        if src and src !="-":
            if isinstance (item ,Script ):

                py_files .append (item )

            elif isinstance (item ,Extension ):
                extensions .append (item )

            else :
                py_files .append (item )


    py_files .sort (key =lambda v :v .filename )
    extensions .sort (key =lambda v :v .filename )
    return py_files ,extensions 


def plat_prepare (includes ,packages ,excludes ):

    includes .update (["warnings","unicodedata","weakref"])

    if not sys .platform .startswith ("irix"):
        excludes .update (["AL","sgi","vms_lib"])

    if sys .platform not in ("mac","darwin"):
        excludes .update (
        [
        "Audio_mac",
        "Carbon.File",
        "Carbon.Folder",
        "Carbon.Folders",
        "EasyDialogs",
        "MacOS",
        "macfs",
        "macostools",
        "_scproxy",
        ]
        )

    if not sys .platform =="win32":

        excludes .update (
        [
        "nturl2path",
        "win32api",
        "win32con",
        "win32event",
        "win32evtlogutil",
        "win32evtlog",
        "win32file",
        "win32gui",
        "win32pipe",
        "win32process",
        "win32security",
        "pywintypes",
        "winsound",
        "win32",
        "_winreg",
        "_winapi",
        "msvcrt",
        "winreg",
        "_subprocess",
        ]
        )

    if not sys .platform =="riscos":
        excludes .update (["riscosenviron","rourl2path"])

    if not sys .platform =="dos"or sys .platform .startswith ("ms-dos"):
        excludes .update (["dos"])

    if not sys .platform =="os2emx":
        excludes .update (["_emx_link"])

    excludes .update (_PLATFORM_MODULES -set (sys .builtin_module_names ))



    excludes .add ("OverrideFrom23")
    excludes .add ("OverrideFrom23._Res")


    excludes .add ("_dummy_threading")

    try :
        imp_find_module ("poll")
    except ImportError :
        excludes .update (["poll"])


def find_needed_modules (
mf =None ,scripts =(),includes =(),packages =(),warn =warnings .warn 
):
    if mf is None :
        mf =modulegraph .ModuleGraph ()


    for path in scripts :
        mf .run_script (path )

    for mod in includes :
        try :
            if mod [-2 :]==".*":
                mf .import_hook (mod [:-2 ],None ,["*"])
            else :
                mf .import_hook (mod )
        except ImportError :
            warn ("No module named %s"%(mod ,))

    for f in packages :



        m =mf .findNode (f )
        if m is not None and m .packagepath is not None :
            path =m .packagepath [0 ]
        else :

            try :
                path =imp_find_module (f ,mf .path )[1 ]
            except ImportError :
                warn ("No package named %s"%f )
                continue 






        for dirpath ,dirnames ,filenames in os .walk (path ):
            if "__init__.py"in filenames and dirpath .startswith (path ):
                package =(
                f 
                +"."
                +dirpath [len (path )+1 :].replace (os .sep ,".")
                )
                if package .endswith ("."):
                    package =package [:-1 ]
                m =mf .import_hook (package ,None ,["*"])
            else :

                dirnames [:]=[]

    return mf 







PY_SUFFIXES =[".py",".pyw",".pyo",".pyc"]

C_SUFFIXES =[
_triple [0 ]for _triple in imp .get_suffixes ()if _triple [2 ]==imp .C_EXTENSION 
]







def _replacePackages ():
    REPLACEPACKAGES ={
    "_xmlplus":"xml",
    }
    for k ,v in REPLACEPACKAGES .items ():
        modulegraph .replacePackage (k ,v )


_replacePackages ()


def find_modules (scripts =(),includes =(),packages =(),excludes =(),path =None ,debug =0 ):
    """
    High-level interface, takes iterables for:
        scripts, includes, packages, excludes

    And returns a :class:`modulegraph.modulegraph.ModuleGraph` instance,
    python_files, and extensions

    python_files is a list of pure python dependencies as modulegraph.Module
    objects, extensions is a list of platform-specific C extension dependencies
    as modulegraph.Module objects
    """
    scripts =set (scripts )
    includes =set (includes )
    packages =set (packages )
    excludes =set (excludes )
    plat_prepare (includes ,packages ,excludes )
    mf =modulegraph .ModuleGraph (
    path =path ,
    excludes =(excludes -includes ),
    implies =get_implies (),
    debug =debug ,
    )
    find_needed_modules (mf ,scripts ,includes ,packages )
    return mf 
