#! /usr/bin/env bash

function test_blue_objects_help() {
    local options=$1

    local module
    for module in \
        "blue_objects"; do
        abcli_eval ,$options \
            $module help
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
