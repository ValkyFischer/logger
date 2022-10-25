import configparser
import os
import traceback
import logging
import tkinter

from logging.config import fileConfig
from datetime import datetime
from time import time
from typing import Union


class UiLogger(logging.Handler):

    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox
        self.textbox.configure(state="disabled")

    def emit(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert(tkinter.END, self.format(text) + "\n")
        self.textbox.see(tkinter.END)
        self.textbox.configure(state="disabled")

    def flush(self):
        pass


class Logger:
    def __init__(self, name: str, path: str = None):

        if path is None:
            path = "./modules/logger/config.ini"
        fileConfig(path)
        self.logger = logging.getLogger(name)

        config = configparser.ConfigParser()
        config.read(path)
        disabled = config['loggers']['disabled'].split(",")
        for logger in disabled:
            no_log = logging.getLogger(logger)
            no_log.setLevel(logging.ERROR)

    @staticmethod
    def recycleLogs(clear: bool = False):
        olf = f"logs/logger.log"
        nlf = f"logs/logger.{int(time())}.log"
        if clear:
            os.remove(olf)
        else:
            os.rename(olf, nlf)

    @staticmethod
    def ProcessMsg(msg: Union[str, tuple, list], kvMsg: dict, addStr: str = None) -> str:
        """
        Build Message

        :param msg: A message that you want to write
        :param kvMsg: key-value type arguments
        :param addStr: Additional string, ex: traceback
        """
        retMsg = f''

        if len(msg) == 1 and isinstance(msg[0], str):
            retMsg += msg[0]
        elif isinstance(msg, tuple) or isinstance(msg, list):
            for item in msg:
                retMsg += f'{str(item)}, '

        for k, v in kvMsg.items():
            retMsg += f'{str(k)}, {str(v)}, '

        if addStr is not None:
            return retMsg[:-2] + f' :: {addStr}'
        elif len(msg) == 1:
            return retMsg
        else:
            return retMsg[:-2]

    def critical(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Critical Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        traceMsg = traceback.format_exc()
        if traceMsg is not None and traceMsg != 'None\n' and traceMsg != 'NoneType: None\n':
            msg = self.ProcessMsg(strMsg, kvStrMsg, traceMsg)
        else:
            msg = self.ProcessMsg(strMsg, kvStrMsg, 'No Traceback')
        self.logger.critical(msg)

    def error(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Error Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        traceMsg = traceback.format_exc()
        if traceMsg is not None and traceMsg != 'None\n' and traceMsg != 'NoneType: None\n':
            msg = self.ProcessMsg(strMsg, kvStrMsg, traceMsg)
        else:
            msg = self.ProcessMsg(strMsg, kvStrMsg, 'No Traceback')
        self.logger.error(msg)

    def warn(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Warning Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.warning(msg)

    def debug(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Debugging Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.debug(msg)

    def info(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Information Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.info(msg)

    def console(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Print Log To Console

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        msgTime = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}]'
        msgLevel = "[CONSOLE]"
        msgName = f"{self.logger.name}:"
        print(msgTime, msgLevel, msgName, msg)
