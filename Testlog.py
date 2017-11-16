from logentries import LogentriesHandler
import logging
import time
LOGENTRIES_TOKEN = "2eda3350-220f-4cee-9560-51642d9dec03"


log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
test = LogentriesHandler(LOGENTRIES_TOKEN)

log.addHandler(test)

log.warn("Warning message")
log.info("Info message")
sleep(10)
