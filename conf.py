#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import sys


class PushConf:

    def __init__(self, conf_file='globe.common.conf'):
        config = configparser.ConfigParser()
        config.read(conf_file)
        self.connect_conf = self.get_connect_conf(config['database_info'])
        self.push_conf = self.get_push_conf(config['tbname_info'])
        self.cron_conf = self.get_cron_conf(config['cron_info'])

    def get_connect_conf(self, section):
        conf = {}


        conf['mysql_ip'] = section.get('MYSQL_IP')
        conf['mysql_port'] = section.get('MYSQL_PORT')
        conf['mysql_user'] = section.get('MYSQL_USER')
        conf['mysql_passwd'] = section.get('MYSQL_PASSWD')
        conf['mysql_db'] = section.get('MYSQL_DB')

        conf['pg_ip'] = section.get('PG_IP')
        conf['pg_port'] = section.get('PG_PORT')
        conf['pg_user'] = section.get('PG_USER')
        conf['pg_passwd'] = section.get('PG_PASSWD')
        conf['pg_db'] = section.get('PG_DB')

        conf['oracle_ip'] = section.get('CRUISE_IP')
        conf['oracle_port'] = section.get('CRUISE_PORT')
        conf['oracle_user'] = section.get('CRUISE_USER')
        conf['oracle_passwd'] = section.get('CRUISE_PASSWD')
        conf['oracle_sid'] = section.get('CRUISE_SID')
        return conf

    def get_push_conf(self, section):
        conf = {}

        conf['focal_region_template'] = section.get('focal_region_template')
        conf['train_push_template'] = section.get('train_push_template')
        conf['flight_push_template'] = section.get('flight_push_template')
        conf['hotel_push_template'] = section.get('hotel_push_template')
        conf['cybercafe_push_template'] = section.get('cybercafe_push_template')
        conf['police_id'] = section.get('police_id')
        return conf

    def get_cron_conf(self, section):
        conf = {}
        conf['cron_day_of_week'] = section.get('cron_day_of_week')
        conf['cron_hour'] = section.get('cron_hour')
        conf['cron_minute'] = section.get('cron_minute')
        return conf


c = PushConf('../conf/globe.common.conf')


class PushCONF:

    def __init__(self):

        self.mysql_ip = c.connect_conf.get('mysql_ip')
        self.mysql_port = c.connect_conf.get('mysql_port')
        self.mysql_user = c.connect_conf.get('mysql_user')
        self.mysql_passwd = c.connect_conf.get('mysql_passwd')
        self.mysql_db = c.connect_conf.get('mysql_db')

        self.pg_ip = c.connect_conf.get('pg_ip')
        self.pg_port = c.connect_conf.get('pg_port')
        self.pg_user = c.connect_conf.get('pg_user')
        self.pg_passwd = c.connect_conf.get('pg_passwd')
        self.pg_db = c.connect_conf.get('pg_db')

        self.oracle_ip = c.connect_conf.get('oracle_ip')
        self.oracle_port = c.connect_conf.get('oracle_port')
        self.oracle_user = c.connect_conf.get('oracle_user')
        self.oracle_passwd = c.connect_conf.get('oracle_passwd')
        self.oracle_sid = c.connect_conf.get('oracle_sid')

        self.focal_region_template = c.push_conf.get('focal_region_template')
        self.train_push_template = c.push_conf.get('train_push_template')
        self.flight_push_template = c.push_conf.get('flight_push_template')
        self.hotel_push_template = c.push_conf.get('hotel_push_template')
        self.cybercafe_push_template = c.push_conf.get('cybercafe_push_template')
        self.police_id = c.push_conf.get('police_id')

        self.cron_day_of_week = c.cron_conf.get('cron_day_of_week')
        self.cron_hour = c.cron_conf.get('cron_hour')
        self.cron_minute = c.cron_conf.get('cron_minute')
