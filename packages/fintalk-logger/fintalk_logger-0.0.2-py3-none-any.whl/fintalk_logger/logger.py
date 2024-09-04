from loguru import logger
import sys
import json
import re
from datetime import datetime, timezone
from .basemodels import *

class Logger():
    def __init__(self):
        self.config = {}
        self.masks = []
        self.logger = logger
        
        logger_config = {'handlers':[{"sink": sys.stdout, "format": "{message}"}]}
        # Add stdout logging
        self.logger.configure(**logger_config)
        
    def reset_config(self):
        self.config = {}
        
    def set_service(self, service:str):
        self.config['service'] = service
        
    def set_request_id(self, request_id:str):
        self.config['request_id'] = request_id
        
    def set_network(self, ip:str):
        network = {
            'client':{ip}
        }
        self.config.network = network
        
    def set_http(self, log_http:LogHttp):
        self.config.http = {
            'useragent':log_http.useragent,
            'method':log_http.method,
            'url':log_http.url
        }
        self.config['host'] = log_http.host
        
    def set_user(self,usr:LogUser):
        self.config['usr'] = usr.dict()
        
    def set_bot(self, bot:str):
        self.config['bot'] = bot
        
    def set_mask(self, masks):
        self.masks = masks
        
    def get_config(self):
        config = {
            # Replicate javascript Date().toISOString() date method
            'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'type':'log',
            **self.config # Dictionary unpacking: https://peps.python.org/pep-0448/
        }
        
        return config
    
    def __format_log(self, log, level):
        formatted_log = {'level':level.upper(), **self.config}
        
        if type(log) == dict:
            formatted_log.update(log)
        elif type(log) == str and level.upper() == 'ERROR':
            formatted_log.update({'err':log})
        else:
            formatted_log.update({'message':log})

        formatted_log = self.__mask_log(formatted_log)
            
        return formatted_log
    
    def __keys_exists(self, element, *keys):
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(element, dict):
            return False
        if len(keys) == 0:
            return False

        # Iterates through dict and checks path
        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True

    
    def __mask_log(self, log):
        '''
        Applies mask to log if key path exists.
        '''
        for mask in self.masks:
            _mask_path_list = mask["path"].split(".")
            if self.__keys_exists(log, *_mask_path_list):
                if log["maskFunction"] == "" or log["maskFunction"] == None:
                    log[mask["path"]] = "*****"
                else:
                    log[mask["path"]] = re.sub(mask["maskFunction"], "*****", log[mask["path"]])
        return log
            
    def trace(self, log):
        log = self.__format_log(log, "TRACE")
        self.logger.trace(json.dumps(log))
        
    def debug(self, log):
        log = self.__format_log(log, "DEBUG")
        self.logger.debug(json.dumps(log))
        
    def info(self, log):
        log = self.__format_log(log, "INFO")
        self.logger.info(json.dumps(log))
        
    def warn(self, log):
        log = self.__format_log(log, "WARN")
        self.logger.warn(json.dumps(log))
        
    def fatal(self, log):
        log = self.__format_log(log, "FATAL")
        self.logger.fatal(json.dumps(log))
        
    def error(self, log):
        log = self.__format_log(log, "ERROR")
        self.logger.error(json.dumps(log))
        
    def set_custom_args(self):
        ...