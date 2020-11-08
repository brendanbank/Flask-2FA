from __future__ import print_function, absolute_import, unicode_literals

from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.client import ClientData
from fido2.server import Fido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2 import cbor
from flask import Flask, session, request, redirect, abort
from fido2.utils import websafe_encode, websafe_decode
from fido2.ctap2 import AttestedCredentialData

import os


class ReplyingPartyServer(object):
    
    def __init__(self,app):
        
        self.app = app
        self.f2fa_manager = app.f2fa_manager
        
        self.publickey = PublicKeyCredentialRpEntity(self.f2fa_manager.F2FA_PK_CREDIENTIAL_ID,  self.f2fa_manager.F2FA_PK_CREDIENTIAL_NAME)
        self.server = Fido2Server(self.publickey)

