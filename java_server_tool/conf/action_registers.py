#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/18
from modules import views

actions = {
    'check_status': views.check_status,
    'stop': views.stop,
    'start': views.start,
    'restart': views.restart,
    'update_service': views.update_service,
    'update_config': views.update_config,
    'roll_back': views.roll_back,

}
