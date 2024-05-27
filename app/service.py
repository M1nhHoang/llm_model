import aiohttp


async def send_messages(messages):
    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            "http://viet_mistral_7b_llm_cpp_service:5005/chat/", json=messages
        ) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status {response.status}")

            # Processing the data stream
            async for data, _ in response.content.iter_chunks():
                yield data
