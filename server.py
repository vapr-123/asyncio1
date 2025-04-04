import asyncio

HOST = 'localhost'
PORT = 9095

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr}")

    print(f"Echoing: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_echo, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())