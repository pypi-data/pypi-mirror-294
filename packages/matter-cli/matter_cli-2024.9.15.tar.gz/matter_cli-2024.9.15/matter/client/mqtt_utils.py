# -*- encoding: utf-8 -*-
'''
@File		:	mqtt_utils.py
@Time		:	2024/09/05 09:52:02
@Author		:	dan
@Description:	MqttClient 实现类
'''
from paho.mqtt import client as mqtt_client
import random
import time

class MqttClient:

    @property
    def protocal(self) -> str:
        '''
        mqtt 协议，mqtt 或 mqtts
        '''
        return self.__protocal

    @property
    def server_host(self) -> str:
        '''
        mqtt 服务器地址
        '''
        return self.__server_host

    @property
    def server_port(self) -> int:
        '''
        mqtt 服务器监听端口
        '''
        return self.__server_port

    '''
    MqttClient 实现类
    '''
    def __init__(self, protocol: str, server_host : str, server_port : str | int = None) -> None:
        '''
        protocal ： 协议，可以是mqtt ，或mqtts
        server_host ： 服务器地址
        server_port ： 服务器监听端口
        ''' 
        if server_port is None:
            if protocol == 'mqtt':
                server_port = 1883
            else:
                server_port = 8883
        
        if server_port is str:
            server_port = int(server_port)


        self.__server_host = server_host
        self.__server_port = server_port
        self.__protocal = protocol
        self.__client : mqtt_client.Client = None



    def connect(self, 
        on_connect = None, 
        keepalive = 60, 
        clean_start = True , 
        username = None, 
        password = None, 
        transport = 'tcp') -> None:
        ''' 连接到mqtt服务器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''

        if keepalive is None:
            keepalive = 60
        if clean_start is None:
            clean_start = True     # MQTT_CLEAN_START_FIRST_ONLY

        client = mqtt_client.Client(
            client_id = "matter." + random.randbytes(32).hex(),
            protocol = mqtt_client.MQTTProtocolVersion.MQTTv5,
            reconnect_on_failure = True,
            transport = transport,

            )
        
        if username is not None and username != '':
            client.username = username
        if password is not None and password != '':
            client.password = password

        self.__client = client
        client.on_connect = on_connect
        client.on_message = self.on_message
        client.connect(self.server_host, self.server_port, keepalive=keepalive, clean_start=clean_start)
        pass


    def on_message(self, client : mqtt_client.Client, userdata : any, message : mqtt_client.MQTTMessage) -> None:
        ''' 
        消息回调
        Parameters
        ----------
        client : mqtt_client.Client,  

        userdata : any, 

        message : mqtt_client.MQTTMessage
        
        Returns
        -------
        None
        
        '''
        
        pass


    def subscribe(self, topic : str) -> tuple[mqtt_client.MQTTErrorCode, int | None]:
        ''' 
        订阅topic
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        return self.__client.subscribe(topic=topic, qos=2)


    def publish(self, topic : str, msg : str, qos: int = 0, retain: bool = False) -> mqtt_client.MQTTMessageInfo:
        '''
        发布消息
        qos: 消息质量
            0 ： 不一定到达
            1 ： 一定到达，但数量不确定
            2： 一定到达，而且有且只有1条达到

        retain : bool 是否保留消息
            true： 保留最新的消息，当订阅消费端服务器重新连接MQTT服务器时，总能拿到该主题最新消息
            false： 不保留最新的消息

        '''
        return self.__client.publish(topic=topic, payload=msg, qos=qos, retain=retain)