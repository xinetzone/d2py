import asyncio, telnetlib3

async def shell(reader, writer):
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        if not outp:
            # End of File
            break
        elif '?' in outp:
            # reply all questions with 'y'.
            writer.write('y')

        # display all server output
        print(outp, flush=True)

    # EOF
    print()

coro = telnetlib3.open_connection('localhost', 6023, shell=shell)

loop = asyncio.get_event_loop()
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)