import subprocess
import os
from tdf_tool.tools.print import Print


class Cmd:
    def run(args, shell=True):
        Print.title("{0}".format(args))
        subprocess_result = subprocess.Popen(
            args, shell=shell, stdout=subprocess.PIPE)
        subprocess_return = subprocess_result.stdout.read()
        return subprocess_return.decode("utf-8")

    def runAndPrint(args, shell=True) -> str:
        result = Cmd.run(args, shell=shell)
        Print.str(result)
        return result

    def system(cmd) -> int:
        Print.step("exec：" + cmd)
        return os.system(cmd)
