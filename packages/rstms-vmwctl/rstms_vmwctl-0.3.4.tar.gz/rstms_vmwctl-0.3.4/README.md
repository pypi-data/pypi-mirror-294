rstms-vmwctl
============


![Image](https://img.shields.io/github/license/rstms/rstms_vmwctl)

![Image](https://img.shields.io/pypi/v/rstms_vmwctl.svg)


VMWare Workstation CLI 

vmctl is inspired by OpenBSD's vmd management utility of the same name.  It aims to 
bring the simplicity and functionality to management of VMWare Workstation VMs.

* Free software: MIT license
* Documentation: https://rstms-vmwctl.readthedocs.io.


# USB security device VMX incantations

Device Name   | VID    | PID 
------------- | ------ | -------
Yubikey 5C    | 1050   | 0407
Ledger Nano S | 2c97   | 5011

```
usb.generic.allowHID = "TRUE"
usb.generic.allowLastHID = "TRUE"
usb.quirks.device0 = "0x1050:0x0407 allow"
usb.quirks.device1 = "0x2c97:0x5011 allow"
usb.autoconnect.device0 = "vid:1050 pid:0407 autoclean:0"
usb.autoconnect.device1 = "vid:2c97 pid:5011 autoclean:0"
```
