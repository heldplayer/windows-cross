FROM ghcr.io/heldplayer/windows-cross-base:main

COPY --chown=root:root bin/xcross-setup /usr/local/bin/xcross-setup
COPY --chown=root:root xcross /xcross/
