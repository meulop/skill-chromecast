# Mycroft AI Chromecast Skill - WIP

A skill to connect with and control a chromecast device connected to the same local network as Mycroft.

This skill is a work in progress and should be considered pre-alpha.  The play media feature is currently hardcoded for testing purposes since it requires a URL.


## TODO

- finish media controller intents
- multi-device-support
- Add youtube and other app support
- remove need for configuration if possible


## Requirements
- [Mycroft](https://docs.mycroft.ai/installing.and.running/installation)
- [Pychromecast](https://github.com/balloob/pychromecast)
- Working Chromecast Device

## Installation

Clone the repository into your skills directory. Then install the
dependencies inside your mycroft virtual environment:

If on picroft just skip the workon part and the directory will be /opt/mycroft/skills

```
cd /opt/mycroft/skills (or wherever your working skills directory is located)
git clone https://github.com/eClarity/skill-chromecast
workon mycroft
cd skill-chromecast
pip install -r requirements.txt
```

## Configuration

Add a block to your Mycroft configuration file like this:

```
  "ChromecastSkill": {
    "cc_device": "YourDeviceName",
  }
```

## Usage:

    list chromecast devices
    play chromecast media
    chromecast device status

