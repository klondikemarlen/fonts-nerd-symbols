#!/usr/bin/env bash
set -euo pipefail

src="${1:-/src}"
work="/tmp/fonts-nerd-symbols-integration"
rm -rf "${work}"
mkdir -p "${work}"
cp -a "${src}/." "${work}/"
cd "${work}"

export DEBIAN_FRONTEND=noninteractive
apt-get update >/dev/null
apt-get install -y --no-install-recommends \
  ca-certificates \
  git \
  xz-utils \
  dpkg-dev \
  devscripts \
  debhelper \
  build-essential \
  fontforge \
  python3-fontforge \
  python3-fonttools \
  debootstrap \
  fontconfig \
  piuparts >/dev/null

make test
./debian/scripts/build-dfsg-package
make test-prepared-source

source_version="$(dpkg-parsechangelog -S Version)"
package_deb="build/fonts-nerd-symbols_${source_version}_all.deb"
test -f "${package_deb}"
python3 tests/check-built-fonts.py "${package_deb}"

apt-get install -y "./${package_deb}"

dpkg -L fonts-nerd-symbols
fc-cache -f
fc-list | grep -i 'Symbols Nerd Font'
fc-match 'Symbols Nerd Font'
fc-match -s 'monospace:charset=e0a0' | grep -m1 -i 'Symbols Nerd Font'

apt-get purge -y fonts-nerd-symbols
piuparts "${package_deb}"
