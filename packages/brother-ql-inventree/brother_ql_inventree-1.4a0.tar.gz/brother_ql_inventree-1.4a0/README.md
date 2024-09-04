# brother_ql-inventree

Python package for the raster language protocol of the Brother QL series label printers


## FORK NOTICE

This is a fork of https://github.com/pklaus/brother_ql by [Philipp Klaus](https://github.com/pklaus) to enable faster updates.
Check out https://github.com/inventree/inventree to see what I forked it for.

## Verified models
### Verified devices

✓ means the device was verified by the original project

QL-500 (✓), QL-550 (✓), QL-560 (✓), QL-570 (✓), QL-580N
QL-600 (✓), QL-650TD
QL-700 (✓), QL-710W (✓), QL-720NW (✓)
QL-800 (✓), QL-810W (✓), QL-820NWB (✓)
QL-1050 (✓), QL-1060N (✓),
QL-1100 (✓), QL-1110NWB, QL-1115NWB.

### Verified labels

The available label names can be listed with `brother_ql info labels`:

     Name      Printable px   Description
     12         106           12mm endless
     12+17      306           12mm endless
     18         234           18mm endless
     29         306           29mm endless
     38         413           38mm endless
     50         554           50mm endless
     54         590           54mm endless
     62         696           62mm endless
     62red      696           62mm endless (black/red/white)
     102       1164           102mm endless
     103       1200           104mm endless
     104       1200           104mm endless
     17x54      165 x  566    17mm x 54mm die-cut
     17x87      165 x  956    17mm x 87mm die-cut
     23x23      202 x  202    23mm x 23mm die-cut
     29x42      306 x  425    29mm x 42mm die-cut
     29x90      306 x  991    29mm x 90mm die-cut
     39x90      413 x  991    38mm x 90mm die-cut
     39x48      425 x  495    39mm x 48mm die-cut
     52x29      578 x  271    52mm x 29mm die-cut
     54x29      598 x  271    54mm x 29mm die-cut
     60x86      672 x  954    60mm x 87mm die-cut
     62x29      696 x  271    62mm x 29mm die-cut
     62x100     696 x 1109    62mm x 100mm die-cut
     102x51    1164 x  526    102mm x 51mm die-cut
     102x152   1164 x 1660    102mm x 153mm die-cut
     103x164   1200 x 1822    104mm x 164mm die-cut
     d12         94 x   94    12mm round die-cut
     d24        236 x  236    24mm round die-cut
     d58        618 x  618    58mm round die-cut
     pt12       - unknown -   12mm endless
     pt18       - unknown -   18mm endless
     pt24       - unknown -   24mm endless
     pt36       - unknown -   36mm endless

### Backends

There are multiple backends for connecting to the printer available (✔: supported, ✘: not supported):

Backend | Kind | Linux | Mac OS | Windows
-------|-------|---------|---------|--------
network (1) | TCP | ✔ | ✔ | ✔
linux\_kernel | USB | ✔ (2) | ✘ | ✘
pyusb (3) | USB | ✔ (3.1) | ✔ (3.2) | ✔ (3.3)

Warning: when using one of the USB backends make sure the Editor Lite feature is turned off (if your model supports it), otherwise the USB Printer interface won't be detected.

## Significant Changes:
v 1.3:
- Added detection of more media and commands to list and configure settings https://github.com/matmair/brother_ql-inventree/pull/57
- Added new cli command for getting the status of printers https://github.com/matmair/brother_ql-inventree/pull/53

v1.2:
- Remove support for Python 2 https://github.com/matmair/brother_ql-inventree/pull/43 / https://github.com/matmair/brother_ql-inventree/pull/45
- Added support for PT-E550W https://github.com/matmair/brother_ql-inventree/pull/44
- Added label support for 12+17 https://github.com/matmair/brother_ql-inventree/pull/42

v1.1:
- Support for Pillow 10.x https://github.com/matmair/brother_ql-inventree/pull/37
v1.0:

- Renamed the package to `brother_ql-inventree` and added a release action https://github.com/matmair/brother_ql-inventree/pull/16
- Added printer support for QL-600 https://github.com/matmair/brother_ql-inventree/pull/17 , PT-P950NW https://github.com/matmair/brother_ql-inventree/pull/6 , QL-1100, L-1100NWB, QL-1115NWB https://github.com/matmair/brother_ql-inventree/pull/18
- Added label support for DK-1234 https://github.com/matmair/brother_ql-inventree/pull/22 , 54x29  https://github.com/matmair/brother_ql-inventree/pull/19 , DK22246 https://github.com/matmair/brother_ql-inventree/pull/20, ...

Read the full old Readme [here](https://github.com/matmair/brother_ql-inventree/blob/cleanup/OLD_README.md).
