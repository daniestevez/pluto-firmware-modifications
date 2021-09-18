# Pluto firmware modifications
Tools and documentation to aid in modifying the ADI ADALM Pluto firmware

## Extraction of the Pluto firmware image

This describes how to extract the individual components of the `pluto.frm`
firmware image. It can be useful if only some of the components are going to be
modified, since it saves us from having to build the rest from source.

Assuming we have the file `pluto.frm` in the same directory as the
`extract_data_dts`, we can create a directory `build` to extract the components
of the FIT image. This needs `dtc`, which is often included in a package called
`device-tree-compiler` in Linux distributions.

```
mkdir build
cd build
dtc -O dts ../pluto.frm | ../extract_data_dts.py /dev/stdin
```

This will extract and the data files inside the FIT image. The filenames of the
extracted files are chosen according to the `description` field in the
corresponding node of the tree. The files need to be renamed according to the
filenames expected by the
[`pluto.its`](https://github.com/analogdevicesinc/plutosdr-fw/blob/master/scripts/pluto.its)
file.

```
for file in zynq-pluto*; do mv $file $file.dtb; done
mv FPGA system_top.bit
mv Linux zImage
mv Ramdisk rootfs.cpio.gz
```

Now we can replace some of these files as required with our modifications, and
build the FIT image and `.frm` file as described in the
[ADI
Wiki](https://wiki.analog.com/university/tools/pluto/building_the_image#build_multi_component_fit_image_flattened_image_tree).

This requires `mkimage`, which is usually contained in the package `uboot-tools`
in Linux distributions.

```
cd ..
mkdir new_frm
cd new_frm
wget https://raw.githubusercontent.com/analogdevicesinc/plutosdr-fw/master/scripts/pluto.its
mkimage -f pluto.its pluto.itb
md5sum pluto.itb | cut -d ' ' -f 1 > pluto.frm.md5
cat pluto.itb pluto.frm.md5 > pluto.frm
```
