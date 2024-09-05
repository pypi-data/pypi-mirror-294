from typing import Any

import typer
from amsdal.manager import AmsdalManager
from amsdal.services.transaction_execution import TransactionExecutionService
from amsdal_data.transactions.background.connections.base import WorkerMode
from amsdal_data.transactions.background.manager import BackgroundTransactionManager
from amsdal_server.apps.transactions.services.transaction_api import TransactionApi
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.errors import AmsdalInitiationError
from rich import print

from amsdal_cli.commands.worker.app import sub_app
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error


@sub_app.command(name='run')
def run_worker(
    ctx: typer.Context,
    mode: WorkerMode = typer.Option(WorkerMode.EXECUTOR, help='Worker mode.'),  # noqa: B008
) -> None:
    """Run worker."""

    cli_config: CliConfig = ctx.meta['config']

    def _init_function(**kwargs: Any) -> None:  # noqa: ARG001
        config_manager = AmsdalConfigManager()
        config_manager.load_config(cli_config.config_path)
        manager = AmsdalManager()

        if not manager.is_setup:
            manager.setup()
            manager.authenticate()

        for transaction in TransactionApi().get_transactions().rows:
            TransactionExecutionService().get_transaction_func(transaction.title)

    _init_function()

    try:
        BackgroundTransactionManager().connection.run_worker(_init_function, mode=mode)
    except AmsdalInitiationError:
        print(rich_error('Worker is not registered.'))
        return
