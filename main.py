from paarser import Parser
import asyncio


async def read_request(parser):
    print('reading thread started')
    while True:
        t = input()
        print('red: ', t)
        parser.add_request(t)


p = Parser()
asyncio.run(read_request(p))
p.start()
