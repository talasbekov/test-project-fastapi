#!/usr/bin/env sh
# check if local github user is not krulwaifu
if [ "$(git config user.email)" == "super.raha2002@gmail.com" ]; then
    echo "YA DAUN"
    exit 1
fi
