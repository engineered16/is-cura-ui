mkdir build
cd build
mkdir files
cp -rfv ../SmartSlicePlugin files/plugins
cp -rfv ../packaging/* .
rm -f ../SmartSlicePlugin-master.zip
zip -rv ../SmartSlicePlugin-master.zip .
cd ..
rm -rfv build
