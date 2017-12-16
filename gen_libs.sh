#!/bin/sh
set -e

echo -n "Downloading header-only libraries..."
mkdir deps
wget https://github.com/nlohmann/json/releases/download/v2.1.1/json.hpp -O deps/json.hpp 2> /dev/null
wget https://github.com/mpark/variant/releases/download/v1.3.0/variant.hpp -O deps/variant.hpp 2> /dev/null
echo " Done."

echo -n "Generating tarball..."
tar czf header_only.tar.gz deps
echo " Done."

echo -n "Removing temporary files..."
rm -rf deps
echo " Done."
