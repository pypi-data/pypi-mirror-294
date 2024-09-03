import asyncio
import multiprocessing

import click
import rich
import sentry_sdk
from sqlalchemy import select

from decentnet.cli.keys import generate_impl
from decentnet.modules.banner.banner import orig_text
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.models import OwnedKeys, AliveBeam
from decentnet.modules.migrate.migrate_agent import MigrateAgent
from decentnet.modules.monitoring.statistics import Stats
from decentnet.modules.seed_connector.SeedsAgent import SeedsAgent
from decentnet.modules.tcp.server import TCPServer

sentry_sdk.init(
    dsn="https://71d6a0d07fac5d2f072b6c7151321766@o4507850186096640.ingest.de.sentry.io/4507850892378192",
)


@click.group()
def service():
    pass


@service.command()
@click.argument('host', type=click.STRING)
@click.argument('port', type=int)
def start(host: str, port: int):
    rich.print(orig_text)
    MigrateAgent.do_migrate()
    multiprocessing.Process(target=Stats.start_prometheus_server).start()
    rich.print("Starting DecentMesh...")
    asyncio.run(__generate_keys())

    server = TCPServer(host, port)
    server_process = multiprocessing.Process(target=server.run)
    server_process.start()
    rich.print("Connecting to DecentMesh seed nodes...")
    SeedsAgent(host, port)


async def __generate_keys():
    async with session_scope() as session:
        result = await session.execute(select(AliveBeam))
        beams = result.scalars().all()

        for beam in beams:
            await session.delete(beam)

        await session.commit()

        # Check for any OwnedKeys asynchronously
        result = await session.execute(select(OwnedKeys).limit(1))
        owned_key = result.scalar_one_or_none()

        if owned_key is None:
            print("Generating first keys for communication")
            generate_impl(private_key_file=None, public_key_file=None, description="First Key", sign=True)
            generate_impl(private_key_file=None, public_key_file=None, description="First Key", sign=True)
            generate_impl(private_key_file=None, public_key_file=None, description="First Key", sign=True)
            generate_impl(private_key_file=None, public_key_file=None, description="First Key", sign=False)
