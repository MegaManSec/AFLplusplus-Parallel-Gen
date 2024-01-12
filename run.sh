#!/bin/bash
IFS=$'\n'

cmds="$(cat -)"

[[ -z "$cmds" ]] && echo "Usage: ./generate.py -n N --fuzz-out <dir> --corpus <dir> --fuzz-loc <loc> --san-fuzz-loc <loc> --cmp-fuzz-loc <loc> | run.sh" && exit 1

while read -r cmd; do
  [[ "$cmd" == *"AFL_AUTORESUME"* ]] || continue
  echo  screen -dmS "screen_main$i" bash -c "$cmd; exec bash"
  ((i++))
done < <(echo -e "$(echo "$cmds" | tail -n 1)\n$(echo "$cmds" | head -n -1)")
