# -*- encoding: utf-8 -*-
'''
@File		:	mqtt.py
@Time		:	2024/09/05 08:56:33
@Author		:	dan
@Description:	mqtt 方法的入口
'''
from matter.manager.group_manager import GroupManager

from paho.mqtt import client as mqtt_client

def publish(topic : str, msg : str, qos: int = 0, retain: bool = False):
    '''
    发布mqtt
    '''
    client = GroupManager().current_client()
    mqtt_client = client.mqtt
    mqtt_client.publish(topic=topic, msg=msg);
    pass

def subscribe(topic : str, ):
    '''
    订阅mqtt
    '''
    client = GroupManager().current_client()
    mqtt_client = client.mqtt
    mqtt_client.subscribe(topic)
    pass