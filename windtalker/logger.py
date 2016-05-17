#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A super easy to use log utility class.

**中文文档**

一个开箱即用的自定义logger类。


Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Python2: Yes
- Python3: Yes


Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- None


Class, method, function, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


from __future__ import print_function
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler


class EZLogger(object):
    """A time roatating logger class.

    :param name: default "root", logger name
    :param path: default None, log file path, default None, do not write to file
    :param logging_level: default "debug", debug level above this will be logged
    :param stream_level: default "info", debug level above this will be printed to console
    :param format: default "%(asctime)s; %(levelname)-8s; %(message)s", log format
    :param rotate_on_when: default "D", EZLogger use time rotate file handler.
      it automatically rotate on "S" for second, "M" for minute, "H" for hour,
      "D" for day.

    Useful method:

    - :meth:`EZLogger.show` display text in standard error, and will not be logged
    - :meth:`EZLogger.kill` kill the log session.
    """
    tab = " " * 4

    def __init__(self, name="root", path=None,
                 logging_level="debug",
                 stream_level="info",
                 format="%(asctime)s; %(levelname)-8s; %(message)s",
                 rotate_on_when="D",
                 ):
        logger = logging.getLogger(name)

        # Logging level and Stream Level
        mapper = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        try:
            logger.setLevel(mapper[logging_level.lower().strip()])

            handler = logging.StreamHandler()
            handler.setLevel(mapper[stream_level.lower().strip()])
            logger.addHandler(handler)
        except KeyError:
            raise KeyError("'logging_level' and 'stream_level' has to be on of"
                           "'debug', 'info', 'warning', 'error', 'critical'!")

        # File handler
        if path:
            if rotate_on_when:
                handler = TimedRotatingFileHandler(  # Time rotate file handler
                    path, when=rotate_on_when, encoding="utf-8")
            else:
                handler = logging.FileHandler(
                    path, mode="a", encoding="utf-8")
            formatter = logging.Formatter(format)  # Formatter
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger
        self.stderr = sys.stderr

    def debug(self, msg, indent=0):
        self.logger.debug("%s%s" % (self.tab * indent, msg))

    def info(self, msg, indent=0):
        self.logger.info("%s%s" % (self.tab * indent, msg))

    def warning(self, msg, indent=0):
        self.logger.warning("%s%s" % (self.tab * indent, msg))

    def error(self, msg, indent=0):
        self.logger.error("%s%s" % (self.tab * indent, msg))

    def critical(self, msg, indent=0):
        self.logger.critical("%s%s" % (self.tab * indent, msg))

    def show(self, msg, indent=0):
        """Print highlighted message to standard error.
        """
        self.stderr.write("%s%s\n" % (self.tab * indent, msg))

    def kill(self):
        """Kill the file handler association. Otherwise, we cannot do anything
        (e.g. backup, rename, etc... )to the log file.
        """
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)


class EZLoggerAnalyzer(object):
    """A log analyzer for EZLogger.
    """

    def filter(self, path, level=None, msg=None, t_lower=None, t_upper=None,
               case_sensitive=True):
        """Filter log message.

        **中文文档**

        根据level名称, message中的关键字, 和log的时间的区间, 筛选出相关的日志
        """
        if level:
            level = level.upper()  # level name has to be capitalized.

        if not case_sensitive:
            msg = msg.lower()

        size = os.path.getsize(path)
        if size > 256 * 1024 ** 2:  # 256MB
            text = "'%s' is a huge file: %s KB, it may takes long time.\n"
            sys.stderr.write(text % (path, size))

        with open(path, "r") as f:
            res = list()  # result
            for line in f:
                try:
                    t, lv, m = [i.strip() for i in line.split(";")]

                    if level:
                        if lv != level:
                            continue

                    if t_lower:
                        if t < t_lower:
                            continue

                    if t_upper:
                        if t > t_upper:
                            continue

                    if msg:
                        if not case_sensitive:
                            m = m.lower()

                        if msg not in m:
                            continue

                    res.append(line)
                except Exception as e:
                    sys.stderr.write("%s\n" % e)

        return "".join(res)


#--- Unittest ---
if __name__ == "__main__":
    import time
    import unittest

    class Unittest(unittest.TestCase):
        def test_all(self):
            logger = EZLogger(name="test", path="test.log")
            logger.debug("Debug message")
            logger.info("Info message", 1)
            logger.warning("Warning message", 2)
            logger.error("Error message", 3)
            logger.critical("Critical message", 4)
            logger.show("Hello World!")
            logger.kill()

            analyzer = EZLoggerAnalyzer()
            print("--- analyze result ---")
            print(
                analyzer.filter("test.log", msg="debug", case_sensitive=False))

        def tearDown(self):
            try:
                os.remove("test.log")
            except Exception as e:
                print(e)

    unittest.main()