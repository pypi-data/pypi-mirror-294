from __future__ import annotations

try:
    from .cppvecchar import CppVector as CppVectorChar
    from .cppvecdouble import CppVector as CppVectorDouble
    from .cppvecfloat import CppVector as CppVectorFloat
    from .cppvecint import CppVector as CppVectorInt
    from .cppveclong import CppVector as CppVectorLong
    from .cppveclong_long import CppVector as CppVectorLongLong
    from .cppvecunsigned_char import CppVector as CppVectorUnsignedChar
    from .cppvecunsigned_int import CppVector as CppVectorUnsignedInt
    from .cppvecunsigned_long import CppVector as CppVectorUnsignedLong
    from .cppvecunsigned_long_long import CppVector as CppVectorUnsignedLongLong
    from .cppvecunsigned_char import CppVector as CppVectorUnsignedChar
    from .cppvecshort import CppVector as CppVectorShort
    from .cppvecunsigned_short import CppVector as CppVectorUnsignedShort
    from .cppvecbyte import CppVector as CppVectorByte
    from .cppvecunsigned_byte import CppVector as CppVectorUnsignedByte
    from .cppveclong_double import CppVector as CppVectorLongDouble
    from .cppvecsize_t  import CppVector as CppVectorSize_t

except Exception as e:
    import Cython, platform, subprocess, os, sys, time, numpy

    iswindows = "win" in platform.platform().lower()
    if iswindows:
        addtolist = []
    else:
        addtolist = ["&"]

    olddict = os.getcwd()
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    compile_file = os.path.join(dirname, "batchcompile.py")
    subprocess._USE_VFORK = False
    subprocess._USE_POSIX_SPAWN = False
    #input('Press Enter to continue...')
    subprocess.run(
        " ".join([sys.executable, compile_file,]),
        shell=True,
        env=os.environ,
        preexec_fn=None
        if iswindows
        else os.setpgrp
        if hasattr(os, "setpgrp")
        else None,
    )
    if not iswindows:
        time.sleep(180)
    from .cppvecchar import CppVector as CppVectorChar
    from .cppvecdouble import CppVector as CppVectorDouble
    from .cppvecfloat import CppVector as CppVectorFloat
    from .cppvecint import CppVector as CppVectorInt
    from .cppveclong import CppVector as CppVectorLong
    from .cppveclong_long import CppVector as CppVectorLongLong
    from .cppvecunsigned_char import CppVector as CppVectorUnsignedChar
    from .cppvecunsigned_int import CppVector as CppVectorUnsignedInt
    from .cppvecunsigned_long import CppVector as CppVectorUnsignedLong
    from .cppvecunsigned_long_long import CppVector as CppVectorUnsignedLongLong
    from .cppvecunsigned_char import CppVector as CppVectorUnsignedChar
    from .cppvecshort import CppVector as CppVectorShort
    from .cppvecunsigned_short import CppVector as CppVectorUnsignedShort
    from .cppvecbyte import CppVector as CppVectorByte
    from .cppvecunsigned_byte import CppVector as CppVectorUnsignedByte
    from .cppveclong_double import CppVector as CppVectorLongDouble
    from .cppvecsize_t  import CppVector as CppVectorSize_t

    os.chdir(olddict)
