# BB Oscilloscope

This is intended to be a BeagleBone Oscilloscope

### Scratchpad Notes


Compiling PRU code from here:
https://github.com/derekmolloy/exploringBB/blob/version1/chp13/prussC/build

```sh
#!/bin/sh
export PRU_SDK=/home/molloyd/pru_2.0.0B2/

echo "Compiling the testPRU.c application"
$PRU_SDK/bin/clpru --silicon_version=3 testPRU.c -i$PRU_SDK/include \
    -i$PRU_SDK/lib -z AM3359_PRU.cmd -o testPRU.out -m testPRU.map

echo "Converting the executable to a ARM object file"
$PRU_SDK/bin/hexpru $PRU_SDK/bin.cmd testPRU.out

echo "Compiling the testBBB.c application"
gcc testBBB.c -o test -lpthread -lprussdrv

echo "Remember to load the overlay from the /chp13/overlay directory using"
echo "   sudo sh -c \"echo EBB-PRU-Example > $SLOTS\""
echo "which requires you to disable the HDMI overlay, as described in Chapter 6"
```

Device Tree Overlay

```
```