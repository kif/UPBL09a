#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import with_statement, print_function

__authors__ = ["Jérôme Kieffer"]
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "10/06/2016"
__status__ = "development"

import os
import unittest
import utilstest
logger = utilstest.getLogger("test_job")
import dahu.job


class TestJob(unittest.TestCase):
    def test_plugin_from_function(self):
        self.called = False
        dico = {"plugin_name": "example.square",
                "x": 5}
        j = dahu.job.Job("example.square", dico)
        j.connect_callback(self.callback)
        logger.info(j)
        j.start()
        j.join()
        logger.info(j)
        if "error" in j.output_data:
            logger.error(os.linesep.join(j.output_data["error"]))

        logger.info(j.input_data)
        assert self.called
        assert j.output_data["result"] == 25

    def callback(self, *args, **kwargs):
        logger.info("callback actually called with  arguments %s and kwargs %s" % (args, kwargs))
        assert len(args) == 1
        self.called = True


def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestJob("test_plugin_from_function"))
    return testSuite

if __name__ == '__main__':
    mysuite = suite()
    runner = unittest.TextTestRunner()
    runner.run(mysuite)
