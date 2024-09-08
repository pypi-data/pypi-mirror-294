import os.path
import sys
from logging import getLogger
from typing import List, Optional

# make sure thonny folder is in sys.path (relevant in dev)
thonny_container = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if thonny_container not in sys.path:
    sys.path.insert(0, thonny_container)

import thonny
from thonny.common import PROCESS_ACK
from thonny.plugins.micropython.os_mp_backend import SshUnixMicroPythonBackend

logger = getLogger("thonny.plugins.ev3.ev3_back")


class EV3MicroPythonBackend(SshUnixMicroPythonBackend):
    def _get_sys_path_for_analysis(self) -> Optional[List[str]]:
        return [
            self.get_user_stubs_location(),
            os.path.join(os.path.dirname(__file__), "api_stubs"),
        ] + super()._get_sys_path_for_analysis()


if __name__ == "__main__":
    thonny.configure_backend_logging()
    print(PROCESS_ACK)

    import ast

    args = ast.literal_eval(sys.argv[1])

    EV3MicroPythonBackend(args)
