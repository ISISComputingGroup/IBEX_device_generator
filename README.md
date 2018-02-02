# IOC_Generator
Generates the boilerplate structure required for developing an IBEX IOC

Run the script with the following command

```
python IBEX_device_generator.py --name=[NAME] --ticket=[TICKET] --device_count=2
```

where:

- **name**: the name of the device. It is used of generating the name of the IOC, the branches it creates, the device emulator etc.
- **ticket**: is the ticket number. It is used for naming the branches created during the script
- **device_count**: the number of IOCs to generate. This argument is optional and defaults to 2

The script runs the following steps:

- Add an EPICS submodule for the device
- Add boilerplate code to the support submodule
- Create `device_count` template IOCs, build them and run `make iocstartups`
- Create a standalone Lewis emulator
- Add a sample test suite to the IOC test framework and add it to `run_all_tests.bat`
- Create a blank OPI and add it to `opi_info.xml`
