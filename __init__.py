# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_handler

import time
import pychromecast

__author__ = 'eClarity'

LOGGER = getLogger(__name__)


class ChromecastSkill(MycroftSkill):
    def __init__(self):
        super(ChromecastSkill, self).__init__(name="ChromecastSkill")
        self.chromecasts = pychromecast.get_chromecasts()

    @intent_handler(IntentBuilder("CCDevicesIntent")
			.require("CCDevicesKeyword"))
    def handle_cc_devices_intent(self, message):
        try:
            self.speak("Searching for Chromecast devices")
            self.chromecasts = pychromecast.get_chromecasts()
            if self.chromecasts is None:
                self.speak_dialog("search.failure")
            else:
                devicecount = len(self.chromecasts)
                plural = (devicecount == 1) ? "" : "s"
                self.speak_dialog("search.success",data = { 'devicecount' : devicecount, 'plural': plural} )
                for cc in self.chromecasts:
                    self.speak(cc.device.friendly_name)
        except:
            self.speak("Something went wrong when trying to find Chromecast devices")

    @intent_handler(IntentBuilder("CCDeviceStatusIntent")
                        .require("CCDeviceStatusKeyword")
                        .require("CCDevice"))
    def handle_cc_device_status_intent(self, message):
        cc_device = message.data.get("CCDevice")
        cast = next(cc for cc in self.chromecasts if cc.device.friendly_name == cc_device)
        cast.wait()
        if cast.status.is_active_input == False:
            self.speak("Your Chromecast device is currently not active")
        elif cast.status.is_active_input == True:
            self.speak("Your Chromecast device is currently active")
        else:
            self.speak("Sorry I had trouble connecting to your chromecast")


    @intent_handler(IntentBuilder("CCMutedIntent")
                        .require("CCMutedKeyword"))
    def handle_cc_muted_intent(self, message):
        cast = next(cc for cc in self.chromecasts if cc.device.friendly_name == "living room")
        cast.wait()
        if cast.status.volume_muted == False:
            self.speak("Your Chromecast device is currently not muted")
        elif cast.status.volume_muted == True:
            self.speak("Your Chromecast device is currently muted")
        else:
            self.speak("Sorry I had trouble connecting to your chromecast")

    @intent_handler(IntentBuilder("CCPlayMediaIntent")
            .require("CCPlayMediaKeyword")
            .require("CCDevice"))
    def handle_cc_play_media_intent(self, message):
        cc_device = message.data.get("CCDevice")
        cast = next(cc for cc in self.chromecasts if cc.device.friendly_name == cc_device)
        mc = cast.media_controller
        self.speak("Playing media on your chromecast now")
        mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
        #mc.block_until_active()

    def stop(self):
        pass


def create_skill():
    return ChromecastSkill()
