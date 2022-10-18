import traceback
import logging

from logging.config import fileConfig
from datetime import datetime
from typing import Union


class Logger:
    def __init__(self, name: str, path: str = None):
        if path is not None:
            fileConfig(path)
        else:
            fileConfig(f"../../modules/logger/config.ini")
        self.logger = logging.getLogger(name)
        self.werkzeug = logging.getLogger("werkzeug")
        self.werkzeug.setLevel(logging.ERROR)

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

    def Critical(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
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

    def Error(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
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

    def Warn(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Warning Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.warning(msg)

    def Debug(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Debugging Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.debug(msg)

    def Info(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
        """
        Write Information Log

        :param strMsg: A message that you want to write
        :param kvStrMsg: key-value type arguments
        """
        msg = self.ProcessMsg(strMsg, kvStrMsg)
        self.logger.info(msg)

    def Console(self, *strMsg: Union[str, int, float], **kvStrMsg: Union[str, int, float]):
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
