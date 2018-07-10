# encoding=utf8
import sys
from resources.parser import AntivirusArgParser
from resources.parser import AntivirusInstallArgParser
from resources.parser import  KkmChangeRequestCreator
__version__ = "1.1"


if __name__ == "__main__":
    args = sys.argv
    if(len(args) > 1):
        del args[0]


    modeDict = {
        "antivirus": AntivirusInstallArgParser,
        "virus":    AntivirusArgParser,
        "kkm" : KkmChangeRequestCreator,

        "version":      None
    }
    if len(args) == 0 or args[0] not in modeDict:
        print("Available commands:\n===================")
        print(", ".join(modeDict.keys()))
        sys.exit(1)

    mode = args[0]
    if mode == "version":
        print("Version {ver}".format(ver=__version__))
        exit(0)
    else:
        parser = modeDict[mode]()
        if not parser.process():
            parser.print_help()


