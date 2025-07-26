from aiomqtt import Client
import asyncio

class MQTTPublisher:
    def __init__(self, hostname, port):
        self.HOSTNAME = hostname
        self.PORT = port

    async def publish(self, topic: str, payload: str | float | int):
        async with Client(hostname=self.HOSTNAME, port=self.PORT) as client:
            await client.publish(topic, payload=str(payload))

async def main():
    client = MQTTPublisher("localhost", 1883)
    await client.publish("test", "Hello World")

if __name__=="__main__":
    asyncio.run(main())