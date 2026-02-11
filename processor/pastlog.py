from metadata import LOCATION, PROJECT_ID
from storage import basic as storage
import syslog
import traceback
from execute_logics import kokkai
import subprocess


storage.set_location(LOCATION)
storage.set_project_id(PROJECT_ID)
try:
    kokkai.execute()
except Exception as e:
    syslog.syslog(r''.join(traceback.format_exception(e)))


subprocess.run(["shutdown", "-h", "now"])
