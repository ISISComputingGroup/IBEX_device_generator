# IOC_Generator
Generates the boilerplate structure required for developing an IBEX IOC. It will only add the items you request by prompting you before each item.

Have EPICS Terminal open for this (You can obtain it for example using C:\Instrument\Apps\EPICS\config_env.bat)
Run the script (e.g. in C:\Instrument\Dev\IBEX_device_generator) with the following command

```
%python3% IBEX_device_generator.py --name=[NAME] --ticket=[TICKET] --device_count=2
```

where:

- **name**: the name of the device. It is used of generating the name of the IOC, the branches it creates, the device emulator etc.
- **ticket**: is the ticket number. It is used for naming the branches created during the script
- **device_count**: the number of IOCs to generate. This argument is optional and defaults to 2

The script runs the following steps:

- Add an EPICS submodule for the device
- Add boilerplate code to the support submodule
  - If you get an error message stating that the directory is not found in `C:\Instrument\Apps\EPICS\support\[ioc name]`, create a folder inside support directory (use name of the ioc, in lower case) and run the script again.
- Create `device_count` template IOCs, build them and run `make iocstartups`
- Create a standalone Lewis emulator
- Add a sample test suite to the IOC test framework and add it to `run_all_tests.bat`
- Create a blank OPI and add it to `opi_info.xml`
