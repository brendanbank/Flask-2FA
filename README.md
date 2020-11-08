# Flask-2FA

## Short Intro

Flask-2FA is an extention of Flask-User. I wanted to see if I could make it more easy to implement hardware tokens as a second factor for authentication. Many laptops and phone have cryptographic hardware on board that allows them to generate tokens are tied to that specific device. This allow you to authenticate with two factors, something you knon (your username and password) and something have (your phone, latop or security token like Yubikey's).

This extention builds havily on the great work that was done for [Flask-Login](https://github.com/maxcountryman/flask-login/) and [Flask-User](https://github.com/lingthio/Flask-User/). And of course the dev teams from [Yubico](https://www.yubico.com/) creating the [python-fido2 package](https://github.com/Yubico/python-fido2) and the [cbor-js](https://github.com/paroga/cbor-js) So my gratitue to all.

This was really a fun exploration project to see if I could implement hardware token 2fa with 'simple' technology. I do not intend to make this an "official" python package. If anyone wants to be my guest. 

## (c)

* python-fido2 - Copyright (c) 2018 Yubico AB - All rights reserved.
* Flask-Login - Copyright (c) 2011 Matthew Frazier
* Flask-User - Copyright (c) 2013 Ling Thio
* Flask-2FA - Copyright (c) 2020 Brendan Bank
* cbor-js - Copyright (c) 2014-2016 Patrick Gansterer <paroga@paroga.com>
