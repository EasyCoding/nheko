#!/bin/sh
set -e

echo -n "Downloading header-only libraries..."
mkdir deps
wget https://github.com/nlohmann/json/releases/download/v3.1.2/json.hpp -O deps/json.hpp 2> /dev/null
wget https://github.com/mpark/variant/releases/download/v1.3.0/variant.hpp -O deps/variant.hpp 2> /dev/null
echo " Done."

echo -n "Generating tarball..."
nf=header_only-$(cat deps/*.hpp | sha256sum | awk '{print substr ($1, 0, 7)}').tar.gz
tar czf header_only.tar.gz deps
mv header_only.tar.gz $nf
echo " Done."

echo -n "Removing temporary files..."
rm -rf deps
echo " Done."

echo "Result: $nf"
