#!/usr/bin/env python3
import asyncio
import logging
import random
from collections import Counter
from pathlib import Path

import aiohttp
from aiohttp import web

import sample_backend

logger = logging.getLogger(__name__)

STATIC_PATH = Path(__file__).parent / "static"
WS_FILE = Path(__file__).parent / 'websocket.html'


async def handler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)
    if not available:
        # This is a regular http request
        with open(WS_FILE, 'rb') as fp:
            return web.Response(body=fp.read(), content_type='text/html')

    # this is a websocket request
    await resp.prepare(request)
    my_id = request.app['counter']['next_client_id']
    request.app['counter']['next_client_id'] += 1

    try:
        logger.info(f'[+{my_id}] Connected.')
        request.app['sockets'].append(resp)
        await resp.send_str("Hi!")
        async for msg in resp:
            if msg.type == aiohttp.WSMsgType.ERROR:
                logger.warning(f'[!{my_id}] Exception: {resp.exception()}')

        logger.info(f'[X{my_id}] Closed.')
        return resp

    finally:
        request.app['sockets'].remove(resp)
        logger.info(f'[-{my_id}] Disconnected.')


def broadcast(sockets, msg):
    logger.debug("> " + msg)
    futs = [ws.send_str(msg) for ws in sockets]
    return asyncio.gather(*futs)


async def on_startup(app):
    app['fut'] = asyncio.create_task(generate_content(app))


async def on_shutdown(app):
    await app['fut']
    for ws in app['sockets']:
        await ws.close()


async def generate_content(app):
    try:
        while True:  # Task automatically cancelled on keyboard interrupt.
            content = sample_backend.foo()
            broadcast(app['sockets'], content)
            await asyncio.sleep(random.uniform(1, 4))
    finally:
        await broadcast(app['sockets'], "Going down!")


def init():
    app = web.Application()

    app['counter'] = Counter(next_client_id=1)
    app['sockets'] = []
    app['done'] = asyncio.Event()

    app.router.add_get('/', handler)
    app.router.add_static("/static/", STATIC_PATH)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
    web.run_app(init())
