import os
import sys
import pkgutil
import pyclbr
import importlib

for mod in pkgutil.iter_modules([os.path.abspath(os.path.dirname(__file__))]):
    clbr = pyclbr.readmodule(mod.name, [mod.module_finder.path, mod.name])
    for cls in clbr:
        if (clbr[cls].super and clbr[cls].super[0] == "KnowledgeBase"):
            imp_cls = importlib.import_module(f".{mod.name}", __name__).__dict__[clbr[cls].name]
            sys.modules[__name__].__setattr__(clbr[cls].name, imp_cls)

del clbr
del cls
del imp_cls
del mod
