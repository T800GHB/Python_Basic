#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:20:36 2016

@author: andrew
"""

import logging


logging.config.fileConfig('./basic_exception/logging.conf',disable_existing_loggers=False) 

logger = logging.getLogger(__name__)

logger.info('Submodel info log information')

def test_logger():
    logger = logging.getLogger(__name__)
    logger.debug('Submodel debug log information')