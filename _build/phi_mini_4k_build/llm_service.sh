#!/bin/bash

# ----------------------------------
# FUNC: STEP1: Cleanup
# example: step_1_cleanup
# ----------------------------------
function llm_service_step_1_cleanup() {
    show_msg_text "[STEP 1/3] Cleanup"

    #1. Xóa docker container
    call_remove_docker_container $DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME

    #2. Xóa docker image
    call_remove_docker_image $DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME

    #3. Xóa docker volume
    call_remove_docker_volume $DOCKER_MINI_4K_LLM_SERVICE_VOLUME_NAME

    #3. Check and create Network
    #call_check_and_create_network $DOCKER_API_SERVICE_NET_WORK

    #4. Check and create Volume
    #call_check_and_create_volume $DOCKER_API_SERVICE_VOLUME_NAME

    show_msg_success "Cleanup thành công."
}


# ----------------------------------
# FUNC: STEP2: Pull Image
# example: step_2_pull_image
# ----------------------------------
function llm_service_step_2_build_image() {
  show_msg_text "[STEP 2/3]: Pull image"

  DOCKERFILE="Dockerfile.llm"
  docker build -f "$(get_source_code_path)/${DOCKER_MINI_4K_LLM_SERVICE_BUILD_PATH}/${DOCKERFILE}" "$(get_relative_path)" -t ${DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME} --no-cache
  check_exists_docker_image_by_name ${DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME}

  if (($? == 1)); then
    show_msg_success "Pull $DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME image thành công."
  else
    show_msg_error "Pull $DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME image thất bại. Vui lòng kiểm tra lại trên Docker."
  fi
}


# ----------------------------------
# FUNC: STEP3: Create container
# example: step_3_create_container
# ----------------------------------
function llm_service_step_3_create_container() {
  show_msg_text "[STEP 3/3]: Create Container"

  check_exists_docker_image_by_name ${DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME}

  if (($? == 1)); then
    #1. Kiểm tra các thành phần đi kèm
    #1.1 Docker network
    # check_exists_docker_network_by_name $DOCKER_API_SERVICE_NET_WORK
    # if (($? == 0)); then
    #   show_msg_text "Không tìm thấy $DOCKER_API_SERVICE_NET_WORK network. Đang thực hiện tạo $DOCKER_API_SERVICE_NET_WORK network ..."
    #   create_docker_network ${DOCKER_API_SERVICE_NET_WORK}
    # fi

    #1.2 Docker volume
    COUNT=$(docker volume ls | grep "$DOCKER_MINI_4K_LLM_SERVICE_VOLUME_NAME" | wc -l)
    if (($COUNT == 0)); then
      show_msg_text "Không tìm thấy $DOCKER_MINI_4K_LLM_SERVICE_VOLUME_NAME volume. Đang thực hiện tạo $DOCKER_MINI_4K_LLM_SERVICE_VOLUME_NAME volume ..."
      create_docker_volume $DOCKER_MINI_4K_LLM_SERVICE_VOLUME_NAME
    fi

    #2. Tạo api container
    #2.1 Tạo mới api container
    VOLUME_PATH="$(get_relative_path)/${DOCKER_MINI_4K_LLM_SERVICE_VOLUME_PATH}"
    docker run -d -ti --name ${DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME} --gpus all --hostname=${DOCKER_MINI_4K_LLM_SERVICE_HOST} -v "${VOLUME_PATH}":/app -p ${DOCKER_MINI_4K_LLM_SERVICE_MACHINE_PORT}:${DOCKER_MINI_4K_LLM_SERVICE_HOST_PORT} ${DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME}
    echo "docker run -ti --name ${DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME} --gpus all --hostname=${DOCKER_MINI_4K_LLM_SERVICE_HOST} -d -v "${VOLUME_PATH}":/app -p ${DOCKER_MINI_4K_LLM_SERVICE_MACHINE_PORT}:${DOCKER_MINI_4K_LLM_SERVICE_HOST_PORT} ${DOCKER_MINI_4K_LLM_SERVICE_IMAGE_NAME}"

    #2.2 Kiểm tra kết quả
    check_exists_docker_container_by_name $DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME
    if (($? == 1)); then
      show_msg_success "Tạo $DOCKER_MINI_4K_LLM_SERVICE_CONTAINER_NAME container thành công."
    fi
  else
    show_msg_error "Không tìm thấy ${DOCKER_API_SERVICE_IMAGE_NAME} image -> Vui lòng kiểm tra lại trên Docker ... "
  fi
}

# ----------------------------------
# FUNC: Setup
# ----------------------------------
function llm_service_setup_env() {
  llm_service_step_1_cleanup
  llm_service_step_2_build_image
  llm_service_step_3_create_container
}