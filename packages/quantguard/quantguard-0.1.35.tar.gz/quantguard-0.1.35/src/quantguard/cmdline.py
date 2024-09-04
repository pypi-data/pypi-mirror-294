import click
from quantguard.config import settings
from quantguard.server import Server


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-V", "--version", is_flag=True, help="Show version and exit.")
def main(ctx, version):
    if version:
        click.echo(settings.VERSION)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option("--level", help="Log level")
@click.option("--work", help="bill, summary")
def server(level, work):
    """Start server."""
    kwargs = {
        "LOGLEVEL": level,
    }
    print(f"work: {work}")
    print(kwargs)
    for name, value in kwargs.items():
        if value:
            settings.set(name, value)
    if work is None or work == "bill":
        Server().run_bill_worker()
