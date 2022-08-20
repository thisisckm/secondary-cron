#!/usr/bin/python
from systems import scheduler, logger
import tasks

import os
import sys
import time

        
if __name__ == '__main__':
    try:
        scheduler.start()
        
        while True:
            wait_sec = os.environ.get('SC_UK_V1_UPDATE_WAIT_SEC', '60')
            wait_sec = int(wait_sec)
            time.sleep(wait_sec)

    except KeyboardInterrupt:
        logger.info('Exiting by user request')
        sys.exit(0)
    except Exception as ex:
        logger.error(str(ex))
        sys.exit(1)