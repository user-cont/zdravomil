#!/bin/bash

set -e

# Generate passwd file based on current uid
function generate_passwd_file() {
  export USER_ID=$(id -u)
  export GROUP_ID=$(id -g)
  grep -v ^zdravomil /etc/passwd > "$HOME/passwd"
  echo "zdravomil:x:${USER_ID}:${GROUP_ID}:Source linter bot:${HOME}:/bin/bash" >> "$HOME/passwd"
  export LD_PRELOAD=libnss_wrapper.so
  export NSS_WRAPPER_PASSWD=${HOME}/passwd
  export NSS_WRAPPER_GROUP=/etc/group
}
