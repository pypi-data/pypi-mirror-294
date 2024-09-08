import os
import subprocess
import sys
import platform
from list_all_files_recursively import get_folder_file_complete_path
import os

iswindows = "win" in platform.platform().lower()
if iswindows:
    addtolist = []
else:
    addtolist = ["&"]
thisfolder = os.path.dirname(os.path.abspath(__file__))
thisfolder_init = os.path.join(thisfolder, "__init__.py")
blueprint_cython = os.path.join(thisfolder, "cppum.pyx")
blueprint_compile = os.path.join(thisfolder, "cppum_compile.py")
importcmds = os.path.join(thisfolder, "allimportcmds.pyx")
relpaths = os.path.join(thisfolder, "allmodules.py")
with open(blueprint_cython, mode="r", encoding="utf-8") as f:
    data = f.read().splitlines()
with open(blueprint_compile, mode="r", encoding="utf-8") as f:
    data2 = f.read().splitlines()
subprocess._USE_VFORK = False
subprocess._USE_POSIX_SPAWN = False
class_name = "CppUMap"

data_types = {
    "int": ("int", "ctypes.c_int32", 'b"%d, "', "int", "l"),
    "unsigned_int": ("unsigned int", "ctypes.c_uint32", 'b"%u, "', "int", "L"),
    "long": ("long", "ctypes.c_int32", 'b"%ld, "', "int", "l"),
    "unsigned_long": ("unsigned long", "ctypes.c_uint32", 'b"%lu, "', "int", "L"),
    "long_long": ("long long", "ctypes.c_int64", 'b"%lld, "', "int", "q"),
    "unsigned_long_long": (
        "unsigned long long",
        "ctypes.c_uint64",
        'b"%llu, "',
        "int",
        "Q",
    ),
    "float": ("float", "ctypes.c_float", 'b"%f, "', "float", "f"),
    "double": ("double", "ctypes.c_double", 'b"%lf, "', "float", "d"),
    "char": ("char", "ctypes.c_char", 'b"%c, "', "str", "b"),
    "unsigned_char": ("unsigned char", "ctypes.c_uint8", 'b"%c, "', "int", "B"),
    "short": ("short", "ctypes.c_int16", 'b"%hd, "', "int", "h"),
    "unsigned_short": ("unsigned short", "ctypes.c_uint16", 'b"%hu, "', "int", "H"),
    "byte": ("char", "ctypes.c_int8", 'b"%h, "', "int", "b"),
    "unsigned_byte": ("unsigned char", "ctypes.c_uint8", 'b"%h, "', "int", "B"),
    "long_double": ("long double", "ctypes.c_longdouble", 'b"%Lg, "', "float", "g"),
    "size_t": ("size_t", "ctypes.c_size_t", 'b"%zu, "', "int", "z"),
    "string": ("string", "ctypes.c_char_p", 'b"%c, "', "bytes", "B"),
}

t = """ctypedef KEYNUMBER0 MY_DATA_TYPE_KEY
ctypedef VALUENUMBER0 MY_DATA_TYPE_VALUE
MY_DATA_TYPE_C_TYPES_KEY=KEYNUMBER1
MY_DATA_TYPE_C_TYPES_VALUE=VALUENUMBER1
#cdef bytes MY_DATA_TYPE_PRINTF_FORMAT = KEYNUMBER2 : VALUENUMBER2"
MY_DATA_TYPE_PY_KEY=type(KEYNUMBER3)
MY_DATA_TYPE_PY_VALUE=type(VALUENUMBER3)
MY_DATA_TYPE_STR_KEY='KEYNUMBER4'
MY_DATA_TYPE_STR_VALUE='VALUENUMBER4'

"""

replaceline = 0
for ini, line in enumerate(data):
    if "#datatypeinfos" in line:
        replaceline = ini
        break
compileline = 0
for ini, line in enumerate(data2):
    if "# modulename" in line:
        compileline = ini
        break
outfiles = {}

prefix = class_name.lower()
folder_prefix = "um"
for k0, v0 in data_types.items():
    for k1, v1 in data_types.items():
        tnew = (
            t.replace("KEYNUMBER0", v0[0])
            .replace("VALUENUMBER0", v1[0])
            .replace("KEYNUMBER1", v0[1])
            .replace("VALUENUMBER1", v1[1])
            .replace("KEYNUMBER2", v0[2][:-3])
            .replace("VALUENUMBER2", v1[2][2:-3])
            .replace("KEYNUMBER3", v0[3])
            .replace("VALUENUMBER3", v1[3])
            .replace("KEYNUMBER4", v0[4])
            .replace("VALUENUMBER4", v1[4])
        )
        datatype1 = v0[1].split(".")[-1]
        datatype2 = v0[1].split(".")[-1]
        foldername = f"{folder_prefix}_{k0}__{k1}".lower()
        full_folder_path = os.path.join(thisfolder, foldername)
        pyx_filename = f"{folder_prefix}.pyx"
        path_pyx = os.path.join(full_folder_path, pyx_filename)
        path_init_file = os.path.join(full_folder_path, "__init__.py")
        filename_compile_short = f"{folder_prefix}_compile.py"
        path_compile_file = os.path.join(full_folder_path, filename_compile_short)
        importcmd = f"""from .{folder_prefix} import {class_name} as Um_{k0.lower()}_{k1.lower()}"""
        outfiles[foldername] = {
            "pyx": data.copy(),
            "comp": data2.copy(),
            "file_pyx": path_pyx,
            "file_comp": path_compile_file,
            "file_comp_short": filename_compile_short,
            "initfile": path_init_file,
            "modulefolderabs": full_folder_path,
            "importcmd": importcmd,
        }
        outfiles[foldername]["pyx"][replaceline] = tnew
        outfiles[foldername]["comp"][compileline] = f'''name = "{folder_prefix}"'''
allimportcmds = []
allrelativepath = []
good_imports = []
bad_imports = []
counterfile = 0
for module, content in outfiles.items():
    os.makedirs(content["modulefolderabs"], exist_ok=True)
    os.chdir(
        content["modulefolderabs"],
    )
    compile_file = content["file_comp_short"]
    with open(content["file_pyx"], mode="w", encoding="utf-8") as f:
        f.write("\n".join(content["pyx"]))
    with open(content["file_comp"], mode="w", encoding="utf-8") as f:
        f.write("\n".join(content["comp"]))
    with open(content["initfile"], mode="w", encoding="utf-8") as f:
        f.write(content["importcmd"])

    dosubi = True
    if dosubi:
        pr = subprocess.run(
            " ".join(
                [sys.executable, compile_file, "build_ext", "--inplace"] + addtolist
            ),
            shell=True,
            env=os.environ,
            preexec_fn=None
            if iswindows
            else os.setpgrp
            if hasattr(os, "setpgrp")
            else None,
            capture_output=True,
        )
        returncode = pr.returncode
        print(pr.stdout)
        print(pr.stderr)
        print(compile_file)
        print(returncode)
        print(f"{counterfile}/{len(outfiles)}")
        counterfile += 1
    else:
        returncode = 0
    if returncode == 0:
        good_imports.append(content["importcmd"])
    else:
        bad_imports.append(content["importcmd"])


os.chdir(thisfolder)
datafolder = thisfolder
inifilestart = os.path.join(datafolder, "__init__.py")
allfiles = get_folder_file_complete_path(datafolder)
nopyending = [x for x in allfiles if "py" not in x.ext.lower()]
for x in nopyending:
    try:
        os.remove(x.path)
    except Exception as e:
        print(f"could not remove: {x.path}")

goodfiles = [
    x for x in get_folder_file_complete_path(datafolder) if x.ext.lower() == ".pyd"
]
for x in goodfiles:
    if r"\build\lib." in x.folder or r"/build/lib" in x.folder:
        try:
            os.remove(x.path)
        except Exception as e:
            print(f"could not remove: {x.path}")

goodfiles = [
    x for x in get_folder_file_complete_path(datafolder) if x.ext.lower() == ".pyd"
]
importstrings = []
for x in goodfiles:
    importstrings.append("from . import " + x.folder.split(os.sep)[-1])

with open(relpaths, mode="w", encoding="utf-8") as f:
    f.write("\n".join(importstrings))

