#!/bin/bash

#
# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Terminate on error
set -e

# Prepare variables for later use
images=()
# The images are pushed to the GitHub container registry
repobase="${REPOBASE:-ghcr.io/geniusdynamics}"
reponame="carbonio-proxy"
# Node.js 25+ no longer ships Corepack, install it from npm
# renovate: datasource=npm packageName=corepack
corepack_version=0.36.0

#
# Carbonio CE runtime image: Ubuntu 22.04 with the pinned Carbonio CE
# packages (see server/Containerfile). Built here and published next to
# the module image, with the same tag.
#
echo "Building the Carbonio CE runtime image..."
buildah build --layers --force-rm \
    --file server/Containerfile \
    --tag "${repobase}/carbonio-proxy-server" \
    server
images+=("${repobase}/carbonio-proxy-server")

# The module reads the Carbonio release and package versions of its runtime
# image, to show them and to refuse a downgrade before restarting
mkdir -p build/etc
server=$(buildah from "${repobase}/carbonio-proxy-server")
buildah run "${server}" cat /usr/share/ns8-carbonio/dist/release.txt >build/etc/carbonio-release
buildah run "${server}" cat /usr/share/ns8-carbonio/packages.txt >build/etc/carbonio-packages.txt
buildah rm "${server}" >/dev/null

# Create a new empty container image
container=$(buildah from scratch)

# Reuse existing nodebuilder-carbonio-proxy container, to speed up builds
if ! buildah containers --format "{{.ContainerName}}" | grep -q nodebuilder-carbonio-proxy; then
    echo "Pulling NodeJS runtime..."
    buildah from --name nodebuilder-carbonio-proxy -v "${PWD}:/usr/src:Z" docker.io/library/node:26.13.0-slim
    buildah run nodebuilder-carbonio-proxy sh -c "npm install -g corepack@${corepack_version} && corepack enable"
fi

echo "Build static UI files with node..."
buildah run \
    --workingdir=/usr/src/ui \
    --env="NODE_OPTIONS=--openssl-legacy-provider" \
    nodebuilder-carbonio-proxy \
    sh -c "yarn install && yarn build"

# Add imageroot directory to the container image
buildah add "${container}" imageroot /imageroot
buildah add "${container}" build/etc /imageroot/etc
buildah add "${container}" ui/dist /ui
#
# - traefik@node:fulladm: web routes, and the certificate of the host name
#   for IMAP and POP3
# - node:fwadm: open the IMAP and POP3 ports
# - carbonio@any:carbonio-peer: obtain the bootstrap secrets from the
#   ns8-carbonio main server (seal-join-bundle)
# - two TCP ports: web client (HTTPS) and Admin Panel, on 127.0.0.1 for Traefik
# - max-per-node=1: the IMAP/POP3 ports and the memcached port are fixed
#
buildah config --entrypoint=/ \
    --label="org.nethserver.authorizations=traefik@node:fulladm node:fwadm carbonio@any:carbonio-peer" \
    --label="org.nethserver.tcp-ports-demand=2" \
    --label="org.nethserver.rootfull=0" \
    --label="org.nethserver.max-per-node=1" \
    --label="org.nethserver.min-core=3.20.1" \
    --label="org.nethserver.images=${repobase}/carbonio-proxy-server:${IMAGETAG:-latest}" \
    "${container}"
# Commit the image
buildah commit "${container}" "${repobase}/${reponame}"

# Append the image URL to the images array
images+=("${repobase}/${reponame}")

#
# Setup CI when pushing to Github.
# Warning! docker::// protocol expects lowercase letters (,,)
if [[ -n "${CI}" ]]; then
    # Set output value for Github Actions
    printf "images=%s\n" "${images[*],,}" >> "${GITHUB_OUTPUT}"
else
    # Just print info for manual push
    printf "Publish the images with:\n\n"
    for image in "${images[@],,}"; do printf "  buildah push %s docker://%s:%s\n" "${image}" "${image}" "${IMAGETAG:-latest}" ; done
    printf "\n"
fi
