#!/bin/bash
# import common
source _bash/_config.cfg
source _bash/_functions.sh

# ----------------------------------
# FUNC: Thực hiện Setup env (local, dev, staging)
# ----------------------------------
function run_setup_phi_mini_4k() {
    MAX_STEP="1"

    # import sas build source
    source phi_mini_4k_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

function run_setup_pho_gpt_vn() {
    MAX_STEP="1"

    # import sas build source
    source pho_gpt_vn_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

# ----------------------------------
# FUNC: Hiển thị menu chọn thao tác
# ----------------------------------
function get_action_init() {
    ACTION_1="Setup phi-mini-4k llm"
    ACTION_2="Setup pho-gpt-vn llm"

    ACTION_LIST="(1, 2)"

    show_msg_confirm "Chọn 1 trong các tác vụ sau (Thao tác chỉ được thực hiện trên local): "
    show_msg_text "1. ${ACTION_1}"
    show_msg_text "2. ${ACTION_2}"

    while true; do
    read -p "${COLOR_TEXT}Nhập tác vụ ${ACTION_LIST} :" action
    case $action in
        [1]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_1}"; run_setup_phi_mini_4k; break;;
        [2]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_2}"; run_setup_pho_gpt_vn; break;;
        * ) show_msg_error "Vui lòng chọn một trong số tác vụ sau: ${ACTION_LIST}";;
    esac
    done
}

get_action_init