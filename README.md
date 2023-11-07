# THIS REPO HAS BEEN ARCHIVED

It will be marked as read-only in case someone wants to fork and restart the effort.

Currently, the Burp plug-in depends on jython, which is now outdated and it has been a year since a formal release. It's likely this will require a complete re-write and/or creating a plugin in Java.

### Defecto-Burp

Defecto-Burp is a Burp Suite plugin used with Burpsuite Professional that support the defectdojo **API v2**.

This extension is designed to export findings to [DefectDojo](https://github.com/DefectDojo/django-DefectDojo).

Features :
* Send findings to existing test
* Create a new test via the Burp plugin
* Supports the defectdojo **API v2**

#### Contribute
Feedback, testing and issue reporting is welcome.

### Installation
In order for the plugin to work , you will need to have Jython set up in Burp Suite Pro .
To use this plugin before it appears in the BApp Store you will need to do the following :
1. Go to `Extender` and select the `Extensions` tab
2. Click on `Add` , select `Extension Type:` to be `Python` and select the `DefectDojoPlugin.py`

![Install Plugin](https://raw.githubusercontent.com/ihebski/Burp-Plugin/master/docs/install-plugin.gif)

### Usage
* Send finding to existing test

![Add finding](https://raw.githubusercontent.com/ihebski/Burp-Plugin/master/docs/add-finding-to-test.gif)

* Send issue As Report (add test)

![send issue As Report](https://raw.githubusercontent.com/ihebski/Burp-Plugin/master/docs/add-test-as-finding.gif)

