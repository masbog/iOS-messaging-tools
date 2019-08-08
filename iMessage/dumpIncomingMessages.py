#!/usr/bin/python
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import frida
import sys

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if isinstance(payload, dict):
            print("to: {}".format(payload.get('toIdentifier', None)))
            print("from: {}".format(payload.get('fromIdentifier', None)))
            print(payload['message'])
        else:
            print(payload)
    else:
        print(message)
    
    if data:
        with open('data', 'wb') as f:
            f.write(data)

if(len(sys.argv) < 2):
    print("Use "+sys.argv[0]+" local or " +sys.argv[0]+" usb")
    sys.exit(0)
elif(sys.argv[1]=="local"):
    session = frida.attach("imagent")
elif(sys.argv[1]=="usb"):
    session = frida.get_usb_device().attach("imagent")


code = open('dumpMessages.js', 'r').read()
script = session.create_script(code);
script.on("message", on_message)
script.load()

print("Press Ctrl-C to quit")
sys.stdin.read()
