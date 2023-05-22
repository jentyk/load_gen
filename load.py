"""Constant load generator."""
import asyncio
import logging
import random
from asyncio import sleep
from collections import Counter
from itertools import cycle

import httpx
import yaml

from config import config

logging.basicConfig(
    level=config.LOG_LEVEL.upper(), format="%(asctime)s %(levelname)s %(message)s"
)


class Loader:
    """Constant load generator."""

    def __init__(self):
        self.resp_stats = Counter()

    async def _send_request(self, url, method, headers, data):
        method_lower = method.lower()
        try:
            async with httpx.AsyncClient() as client:
                method = getattr(client, method_lower)
                if method_lower == "get":
                    response = await method(url, headers=headers, params=data)
                elif method_lower in ("put", "post"):
                    response = await method(url, headers=headers, data=data)
                elif method_lower in ("delete", "head", "options"):
                    response = await method(url, headers=headers)
                self.resp_stats[response.status_code] += 1
        except httpx.RequestError as e:
            logging.error(f"HTTP Exception for {e.request.url} - {e}")

    async def generate_load(self, loop):
        """Send API requests in infinite loop."""
        sleep_time = 1 / config.FREQUENCY
        request_cycler = cycle(config.REQUESTS)
        for burst in cycle(config.CONCURRENT):
            for _ in range(burst):
                request = next(request_cycler)
                loop.create_task(
                    self._send_request(
                        request["url"],
                        request["http_method"],
                        request["headers"],
                        request["data"],
                    )
                )
            await sleep(
                random.uniform(0, sleep_time)
                if config.RANDOMIZE_FREQUENCY
                else sleep_time
            )


def main():
    """Run constant load generator."""
    logging.info("Start loading")
    loader = Loader()
    try:
        with asyncio.Runner(debug=None) as runner:
            runner.run(loader.generate_load(runner.get_loop()))
        return loader.resp_stats
    except (asyncio.CancelledError, KeyboardInterrupt):
        logging.info(
            f"Stop loading.\n\nLoading stats:\n" f"{yaml.dump(dict(loader.resp_stats))}"
        )


if __name__ == "__main__":
    main()
