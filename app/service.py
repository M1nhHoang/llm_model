import aiohttp


async def send_messages(messages, model_service_docker_name, port):
    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            f"http://{model_service_docker_name}:{port}/chat/", json=messages
        ) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status {response.status}")

            # Processing the data stream
            async for data, _ in response.content.iter_chunks():
                yield data
