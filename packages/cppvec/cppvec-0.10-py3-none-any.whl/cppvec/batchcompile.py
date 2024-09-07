import os
import subprocess
import sys
import platform
iswindows = "win" in platform.platform().lower()
if iswindows:
    addtolist = []
else:
    addtolist = ["&"]
thisfolder=os.path.dirname(os.path.abspath(__file__))
blueprint_cython=os.path.join(thisfolder,'cppvect.pyx')
blueprint_compile=os.path.join(thisfolder,'cppvect_compile.py')
with open(blueprint_cython,mode='r',encoding='utf-8') as f:
    data=f.read().splitlines()
with open(blueprint_compile,mode='r',encoding='utf-8') as f:
    data2=f.read().splitlines()
subprocess._USE_VFORK = False
subprocess._USE_POSIX_SPAWN = False
data_types = {
    'int': ('int', 'ctypes.c_long', 'b"%d, "', 'int', 'l'),
    'unsigned_int': ('unsigned int', 'ctypes.c_uint', 'b"%u, "', 'int', 'L'),
    'long': ('long', 'ctypes.c_long', 'b"%ld, "', 'int', 'l'),
    'unsigned_long': ('unsigned long', 'ctypes.c_ulong', 'b"%lu, "', 'int', 'L'),
    'long_long': ('long long', 'ctypes.c_longlong', 'b"%lld, "', 'int', 'q'),
    'unsigned_long_long': ('unsigned long long', 'ctypes.c_ulonglong', 'b"%llu, "', 'int', 'Q'),
    'float': ('float', 'ctypes.c_float', 'b"%f, "', 'float', 'f'),
    'double': ('double', 'ctypes.c_double', 'b"%lf, "', 'float', 'd'),
    'char': ('char', 'ctypes.c_char', 'b"%c, "', 'str', 'b'),
    'unsigned_char': ('unsigned char', 'ctypes.c_ubyte', 'b"%c, "', 'int', 'B'),
    'short': ('short', 'ctypes.c_short', 'b"%hd, "', 'int', 'h'),
    'unsigned_short': ('unsigned short', 'ctypes.c_ushort', 'b"%hu, "', 'int', 'H'),
    'byte': ('char', 'ctypes.c_byte', 'b"%h, "', 'int', 'b'),
    'unsigned_byte': ('unsigned char', 'ctypes.c_ubyte', 'b"%h, "', 'int', 'B'),
    'long_double': ('long double', 'ctypes.c_longdouble', 'b"%Lg, "', 'float', 'g'),
    'size_t': ('size_t', 'ctypes.c_size_t', 'b"%zu, "', 'int', 'z'),
}

t="""ctypedef NUMBER0 MY_DATA_TYPE
MY_DATA_TYPE_C_TYPES=NUMBER1
cdef bytes MY_DATA_TYPE_PRINTF_FORMAT = NUMBER2
cdef int MY_DATA_TYPE_PRINTF_LF = 80
MY_DATA_TYPE_PY=type(NUMBER3)
MY_DATA_TYPE_STR='NUMBER4'"""
replaceline=0
for ini,line in enumerate(data):
    if '#datatypeinfos' in line:
        replaceline=ini
        break
compileline=0
for ini,line in enumerate(data2):
    if '#modulename' in line:
        compileline=ini
        break
outfiles={}
for k,v in data_types.items():
    tnew=(t.replace('NUMBER0',v[0]).replace('NUMBER1',v[1]).replace('NUMBER2',v[2]).replace('NUMBER3',v[3]).replace('NUMBER4',v[4]))
    print(tnew)
    moname='cppvec'+k
    filename=os.path.join(thisfolder,moname+'.pyx')
    filename_compile=os.path.join(thisfolder,moname+'_compile.py')
    filename_compile_short=moname+'_compile.py'
    print(filename)
    outfiles[moname]={'pyx':data.copy(),'comp':data2.copy(),'file_pyx':filename,'file_comp':filename_compile,'file_comp_short':filename_compile_short}
    outfiles[moname]['pyx'][replaceline]=tnew
    outfiles[moname]['comp'][compileline]=f'''name = "{moname}"'''

for module,content in outfiles.items():
    os.chdir(thisfolder)
    compile_file = content['file_comp_short']

    with open(content['file_pyx'],mode='w',encoding='utf-8') as f:
        f.write('\n'.join(content['pyx']))
    with open(content['file_comp'],mode='w',encoding='utf-8') as f:
        f.write('\n'.join(content['comp']))
    subprocess.run(
        " ".join([sys.executable, compile_file, "build_ext", "--inplace"] + addtolist),
        shell=True,
        env=os.environ,
        preexec_fn=None
        if iswindows
        else os.setpgrp
        if hasattr(os, "setpgrp")
        else None,
    )