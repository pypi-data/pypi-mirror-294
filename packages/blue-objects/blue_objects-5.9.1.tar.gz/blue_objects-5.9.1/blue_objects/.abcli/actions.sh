#! /usr/bin/env bash

function blue_objects_action_git_before_push() {
    [[ "$(abcli_git get_branch)" == "main" ]] &&
        blue_objects pypi build
}
