import sys
from loguru import logger
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
        
    def set_mask(self, masks:MaskList):
        for mask in masks:
            if "maskFunction" in mask:
                self.masks.append({"path": mask["path"], "maskFunction":mask["maskFunction"]})
            else:
                self.masks.append({"path": mask["path"], "maskFunction":None})
        
    def get_config(self):
        config = {
            # Replicate javascript Date().toISOString() date method
            'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'type':'log',
            **self.config # Dictionary unpacking: https://peps.python.org/pep-0448/
        }
        
        return config
            
    def trace(self, log):
        log = self.__format_log(log, "TRACE")
        self.logger.trace(log)
        
    def debug(self, log):
        log = self.__format_log(log, "DEBUG")
        self.logger.debug(log)
        
    def info(self, log):
        log = self.__format_log(log, "INFO")
        self.logger.info(log)
        
    def warn(self, log):
        log = self.__format_log(log, "WARN")
        self.logger.warning(log)
        
    def fatal(self, log):
        log = self.__format_log(log, "FATAL")
        self.logger.fatal(log)
        
    def error(self, log):
        log = self.__format_log(log, "ERROR")
        self.logger.error(log)
        
    def set_custom_args(self):
        ...

    def __format_log(self, log, level):
        formatted_log = {'level':level.upper(), **self.config}
        
        if type(log) == dict:
            formatted_log.update(log)
        elif type(log) == str and level.upper() == 'ERROR':
            formatted_log.update({'err':log})
        else:
            formatted_log.update({'message':log})

        formatted_log = self.__mask_log(formatted_log)
        formatted_log = self.__dict_to_str(formatted_log)
        
        return formatted_log
    
    def __dict_to_str(self, log):
        return json.dumps(log)

    def __deep_update(self, mapping, path, mask_function):
        updated_mapping = mapping.copy()
        if path[0] in updated_mapping and isinstance(updated_mapping[path[0]], dict) and len(path)>1:
            updated_mapping[path[0]] = self.__deep_update(updated_mapping[path[0]], path[1:], mask_function)
        else:
            if mask_function == None or mask_function == "":
                updated_mapping[path[0]] = "***"
            else:
                updated_mapping[path[0]] = mask_function(updated_mapping[path[0]])
        
        return updated_mapping
    
    def __keys_exists(self, element, keys):
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
            mask_path_list = mask["path"].split(".")
            mask_function = mask["maskFunction"]
            if self.__keys_exists(log, mask_path_list):
                log = self.__deep_update(log, mask_path_list, mask_function)
        return log