import six
from enum import Enum, unique

class _StringEnum(six.text_type, Enum):
    @classmethod
    def _wrap(cls, value):
        if value is None:
#             return None
            return cls('None')
        return cls(value)
@unique
class AuthenitcatorTokenType(_StringEnum):
    PLATFORM = "platform"
    CROSS_PLATFORM = "cross-platform"
    ANY = None



class F2fa_config(object):
    
    AUTHENTICATOR_TYPE = None
    
#     authenticator_type = AuthenitcatorTokenType('None')
#       
#     #         authenticator_attachment="cross-platform",
#     F2FA_AUTHENTICATOR_TOKEN_TYPES = {}
#     F2FA_AUTHENTICATOR_TOKEN_TYPES['CROSS_PLATFORM'] = 'cross-platform'
#     F2FA_AUTHENTICATOR_TOKEN_TYPES['PLATFORM'] = 'platform'
#     F2FA_AUTHENTICATOR_TOKEN_TYPES['ANY'] = 'any'
#   
#     def __init__(self,authenticator_type=None):
#         self.authenticator_type = authenticator_type
#           
#   
# if __name__ == '__main__':
#       
#     test = F2fa_config()
#     test.authenticator_type = "cross-platform"
#       
#     authenticator_attachment = 'cross-platform'
# #     authenticator_attachment = None
#     authenticator_attachment=AuthenitcatorTokenType._wrap(
#                     authenticator_attachment
#             )
#         
#     if (AuthenitcatorTokenType.PLATFORM == authenticator_attachment):
#         print (True)
#     else:
#         print (False)
#         
#     print (authenticator_attachment.value)
#     
#     condition1 = None
#     condition2 = None
#     condition3 = True
#     condition4 = True
#     
#     print (True) if any((condition1, condition2, condition3))  else None
#     print ((condition1, condition2, condition3))