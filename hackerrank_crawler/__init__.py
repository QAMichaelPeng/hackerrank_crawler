import logging
from scrapy.log import ScrapyFileLogObserver
import settings

if settings.LOG_FILE <> settings.LOG_OBSERVE_FILE:
    logfile = open(settings.LOG_OBSERVE_FILE, 'w')
    log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
    log_observer.start()
