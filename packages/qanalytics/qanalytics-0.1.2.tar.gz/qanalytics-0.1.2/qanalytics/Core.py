import ctypes
import json
import sys
import os

from qanalytics.Struct import *
from qanalytics.Enum import *

def Request(pPath, pArgs, pLogger):

    # load library.
    LibraryExt = '' 
    if sys.platform == 'linux' or sys.platform == 'linux2':
        LibraryExt = 'so'
    elif sys.platform == 'darwin':
        LibraryExt = 'dylib'
    elif sys.platform == 'win32':
        LibraryExt = 'dll'
    LibraryPath = os.path.dirname(__file__) + '\\qAPI.' + LibraryExt
    if not os.path.isfile(LibraryPath):
        raise Exception("dll not found: " + LibraryPath)
    Library = ctypes.CDLL(LibraryPath)

    # set function prototype.
    Function = getattr(Library, "Request")
    Function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    Function.restype = ctypes.c_bool

    # prepare path.
    PathPtr = pPath.encode('utf-8')

    # prepare request.
    RequestDict = {}
    RequestDict['Logger'] = pLogger.serialize()
    for ArgName, ArgStruct in pArgs:
        RequestDict[ArgName] = ArgStruct.serialize()   
    RequestStr = json.dumps(RequestDict)
    RequestPtr = ctypes.c_char_p(RequestStr.encode())

    # prepare response.
    ResponseSize = 2 * len(RequestStr) * sys.getsizeof(ctypes.c_char_p)
    ResponsePtr = ctypes.create_string_buffer(ResponseSize)

    # execute request.
    Success = Function(PathPtr, RequestPtr, ResponsePtr)

    # set results.
    if ResponsePtr != None:
        ResponseStr = ResponsePtr.value.decode('utf-8')
        if ResponseStr != '':
            try:
                ResponseDict = json.loads(ResponseStr)
                pLogger.deserialize(ResponseDict['Logger'])
                if Success:
                    for ArgName, ArgStruct in pArgs:
                        ArgStruct.deserialize(ResponseDict[ArgName])
                    return True
                else:
                    return False
            except json.decoder.JSONDecodeError:
                raise Exception(pPath + ': Cannot decode JSON response')
        else:
            raise Exception(pPath + ': Cannot read response')
    else:
        raise Exception(pPath + ': Cannot read response')

def GetConnectionStatus(pDataConfiguration, pLogger):
    return Request(
        '/GetConnectionStatus',
        [('DataConfiguration', pDataConfiguration)],
        pLogger
    )

def GetContract(pDataConfiguration, pContractConfiguration, pResults, pLogger):
    return Request(
        '/GetContract',
        [('DataConfiguration', pDataConfiguration), ('ContractConfiguration', pContractConfiguration), ('Contract', pResults)],
        pLogger
    )