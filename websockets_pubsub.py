#!/usr/bin/env python3
import asyncio
import logging
from collections import Counter
from pathlib import Path

import aiohttp
from aiohttp import web

logger = logging.getLogger(__name__)

STATIC_PATH = Path(__file__).parent / "static"
WS_FILE = Path(__file__).parent / 'websocket.html'


async def sign_handler(request):
    """Signs (subscribers) should use this handler"""
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


async def publisher_handler(request):
    data = await request.post()
    content = data.get("content")
    if content:
        broadcast(request.app['sockets'], content)
    return web.Response(text="OK")


async def on_shutdown(app):
    for ws in app['sockets']:
        await ws.close()


def init():
    app = web.Application()

    app['counter'] = Counter(next_client_id=1)
    app['sockets'] = []
    app['done'] = asyncio.Event()

    app.router.add_get('/', sign_handler)
    app.router.add_post('/publish/', publisher_handler)
    app.router.add_static("/static/", STATIC_PATH)

    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
    web.run_app(init())
