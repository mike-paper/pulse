import logging
import sys

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug('debugging...')
