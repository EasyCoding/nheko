#!/bin/sh
set -e

echo -n "Setting some constants..."
RESDIR=include
echo " Done."

echo -n "Downloading header-only libraries..."
mkdir $RESDIR
wget https://github.com/nlohmann/json/releases/download/v3.1.2/json.hpp -O $RESDIR/json.hpp 2> /dev/null
wget https://github.com/mpark/variant/releases/download/v1.3.0/variant.hpp -O $RESDIR/variant.hpp 2> /dev/null
echo " Done."

echo -n "Generating tarball..."
nf=header_only-$(cat $RESDIR/*.hpp | sha256sum | awk '{print substr ($1, 0, 7)}').tar.gz
tar czf header_only.tar.gz $RESDIR
mv header_only.tar.gz $nf
echo " Done."

echo -n "Removing temporary files..."
rm -rf $RESDIR
echo " Done."

echo "Result: $nf"
