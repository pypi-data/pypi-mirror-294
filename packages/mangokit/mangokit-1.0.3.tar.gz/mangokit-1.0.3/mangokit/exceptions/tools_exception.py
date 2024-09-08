# -*- coding: utf-8 -*-
# @Project: MangoActuator
# @Description: 
# @Time   : 2023-07-16 15:17
# @Author : 毛鹏
from mangokit.exceptions import TestKitError


class MysqlAbnormalConnection(TestKitError):
    pass


class MysqlQueryIsNullError(TestKitError):
    pass


class MysqlConnectionError(TestKitError):
    pass


class SyntaxErrorError(TestKitError):
    pass


class JsonPathError(TestKitError):
    pass


class JsonSerializeError(TestKitError):
    pass


class CacheKetNullError(TestKitError):
    pass


class ValueTypeError(TestKitError):
    pass


class SendMessageError(TestKitError):
    pass


class DoesNotExistError(TestKitError):
    pass


class MysqlConfigError(TestKitError):
    pass


class MySQLConnectionFailureError(TestKitError):
    pass


class MysqlQueryError(TestKitError):
    pass


class FileDoesNotEexistError(TestKitError):
    pass


class CacheIsEmptyError(TestKitError):
    pass


class SocketClientNotPresentError(TestKitError):
    pass


class InsideSaveError(TestKitError):
    pass


class MiniIoConnError(TestKitError):
    pass


class MiniIoFileError(TestKitError):
    pass


class TestObjectNullError(TestKitError):
    pass


class MethodDoesNotExistError(TestKitError):
    pass


class UserEmailIsNullError(TestKitError):
    pass
