from wsvcs.server import Server
from wsvcs.client import Client
from wsvcs.shared.modes import Mode
from wsvcs import MODE, LAST_HOST, LAST_PROJECT_PATH

import asyncio


async def cli():
    service = None

    match MODE:
        case Mode.SERVER:
            service = Server()
        case Mode.CLIENT:
            service = Client(last_host=LAST_HOST, last_project_path=LAST_PROJECT_PATH)

    await service.run()


def main():
    asyncio.run(cli())


if __name__ == '__main__':
    main()
