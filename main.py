from paarser import Parser
import asyncio


async def read_request(parser):
    print('reading thread started')
    while True:
        t = input()
        print('red: ', t)
        parser.add_request(t)


async def start_parser(parser):
    p.start()



p = Parser()
reader = asyncio.get_event_loop().create_task(read_request(p))
parser = asyncio.get_event_loop().create_task(start_parser(p))
asyncio.get_event_loop().run_until_complete(asyncio.wait([reader]))
# p.start()
