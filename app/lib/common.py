import random


def trueReturn(msg='', data=''):
    return {
        'status':True,
        'msg':msg,
        'data':data
    }


def falseReturn(msg='', data=''):
    return {
        'status':False,
        'msg':msg,
        'data':data
    }


def generate_uid():
    """ example: QxWc512356"""
    uid = ""
    for i in range(0, 2):
        AZ = chr(random.randint(65, 90))
        az = chr(random.randint(97, 122))
        uid = uid + AZ + az
    d = str(random.randint(100000, 999999))
    return uid + d


