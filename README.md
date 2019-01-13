# BB Oscilloscope

This is intended to be a BeagleBone Oscilloscope

## Install needed deps:
- `pip3 install ansible`
- `apt-get install sshpass`

## Useful Links on PRU whatnot:

https://markayoder.github.io/PRUCookbook/

Compiling PRU code from here:
https://github.com/derekmolloy/exploringBB/blob/version1/chp13/prussC/build

## Scratchpad Notes

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

### Building libffi


```bash
git clone git@github.com:libffi/libffi.git
cd libffi
./configure

# Doc generation fails, building text support is hard, remove it
cd armv7l-unknown-linux-gnueabihf/doc
sed -e 's|^MAKEINFO =*|MAKEINFO = true|g' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
cd ../..

make
sudo make install
```
