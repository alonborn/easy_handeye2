#!/usr/bin/env python

import sys
import debugpy
from rqt_gui.main import Main


# debugpy.listen(("localhost", 5678))  # Port for debugger to connect
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client()  # Ensures the debugger connects before continuing
# print("Debugger connected.")


main = Main()
sys.exit(main.main(sys.argv, standalone='easy_handeye2.handeye_rqt_calibrator.RqtHandeyeCalibrator'))
