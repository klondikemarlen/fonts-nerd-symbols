#!/usr/bin/env bash
set -euo pipefail

src="${1:-/src}"
work="/tmp/fonts-nerd-symbols-repro"
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
  fontconfig \
  reprotest \
  faketime \
  disorderfs \
  diffoscope-minimal >/dev/null

source_tree_version="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
./debian/scripts/prepare-upstream "${source_tree_version}" dfsg
cd "build/fonts-nerd-symbols-${source_tree_version}"

reprotest \
  --vary=-domain_host,-user_group \
  'debuild -us -uc -b' \
  '../*.deb'
