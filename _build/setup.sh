#!/bin/bash
# import common
source _bash/_config.cfg
source _bash/_functions.sh

# ----------------------------------
# FUNC: Thực hiện Setup env (local, dev, staging)
# ----------------------------------
function run_setup_web_api() {
    MAX_STEP="1"

    # import sas build source
    source app_build/web_api_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup app api service"
    app_service_setup_env
}

function run_setup_phi_mini_4k() {
    MAX_STEP="1"

    # import sas build source
    source phi_mini_4k_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

function run_setup_phi_mini_4k_cpp() {
    MAX_STEP="1"

    # import sas build source
    source phi_mini_4k_cpp_build/llm_service.sh

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

function run_setup_pho_gpt_vn_cpp() {
    MAX_STEP="1"

    # import sas build source
    source pho_gpt_vn_cpp_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

function run_setup_viet_mistral_7b() {
    MAX_STEP="1"

    # import sas build source
    source viet_mistral_7b_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

function run_setup_viet_mistral_7b_cpp() {
    MAX_STEP="1"

    # import sas build source
    source viet_mistral_7b_cpp_build/llm_service.sh

    show_msg_title "[STEP 1/${MAX_STEP}] Setup llm service"
    llm_service_setup_env
}

# ----------------------------------
# FUNC: Hiển thị menu chọn thao tác
# ----------------------------------
function get_action_init() {
    ACTION_1="Setup web api"
    ACTION_2="Setup phi-mini-4k llm"
    ACTION_3="Setup phi-mini-4k-cpp llm"
    ACTION_4="Setup pho-gpt-vn llm"
    ACTION_5="Setup pho-gpt-vn-cpp llm"
    ACTION_6="Setup viet-mistral-7b llm"
    ACTION_7="Setup viet-mistral-7b-cpp llm"

    ACTION_LIST="(1, 2, 3, 4, 5, 6, 7)"

    show_msg_confirm "Chọn 1 trong các tác vụ sau (Thao tác chỉ được thực hiện trên local): "
    show_msg_text "1. ${ACTION_1}"
    show_msg_text "2. ${ACTION_2}"
    show_msg_text "3. ${ACTION_3}"
    show_msg_text "4. ${ACTION_4}"
    show_msg_text "5. ${ACTION_5}"
    show_msg_text "6. ${ACTION_6}"
    show_msg_text "7. ${ACTION_7}"

    while true; do
    read -p "${COLOR_TEXT}Nhập tác vụ ${ACTION_LIST} :" action
    case $action in
        [1]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_1}"; run_setup_web_api; break;;
        [2]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_2}"; run_setup_phi_mini_4k; break;;
        [3]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_3}"; run_setup_phi_mini_4k_cpp; break;;
        [4]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_4}"; run_setup_pho_gpt_vn; break;;
        [5]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_5}"; run_setup_pho_gpt_vn_cpp; break;;
        [6]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_6}"; run_setup_viet_mistral_7b; break;;
        [7]* ) show_msg_text "Bắt đầu thực hiện ${ACTION_7}"; run_setup_viet_mistral_7b_cpp; break;;
        * ) show_msg_error "Vui lòng chọn một trong số tác vụ sau: ${ACTION_LIST}";;
    esac
    done
}

get_action_init