import sys, inspect
def cList(name="__main__"):
    cList = {}
    for name, obj in inspect.getmembers(sys.modules[name]):
        if inspect.isclass(obj):
            cList[obj.__name__] = obj
    return cList
