from config import config
from mqtt_as import MQTTClient
import uasyncio as asyncio

def callback(topic, msg, retained):
    print((topic, msg, retained))

async def conn_han(client):
    await client.subscribe('foo_topic', 1)
    async def main(client):
        await client.connect()
        n = 0
        while True:
            await asyncio.sleep(5)
            print('publish', n)
            # If WiFi is down the following will pause for the duration.
            await client.publish('result', '{}'.format(n), qos = 1)
            n += 1
            config['subs_cb'] = callback
            config['connect_coro'] = conn_han
            MQTTClient.DEBUG = True
            # Optional: print diagnostic messages

client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(client))
finally:
    client.close()
