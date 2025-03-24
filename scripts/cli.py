import os
import click
from dotenv import load_dotenv
import requests

from models.data import SerialDriverConfig
from models.http import CommandRequest, DeleteDeviceRequest, RegisterDeviceRequest

load_dotenv()


@click.group()
def cli():
    pass


DEVICE_MANAGER_PORT = os.environ["DEVICE_MANAGER_PORT"]
DEVICE_MANAGER_HOST = os.environ["DEVICE_MANAGER_HOST"]

DEVICE_MANAGER_URL = f"http://{DEVICE_MANAGER_HOST}:{DEVICE_MANAGER_PORT}"


@click.command()
@click.option("--name", prompt="Device name", help="The port of the HTTP server.")
@click.option("--type", prompt="Connection Type", help="The port of the HTTP server.")
def register_device(name, type):
    req = RegisterDeviceRequest(
        name=name,
        connection_type=type,
        config=SerialDriverConfig(port="COM1", baudrate=9600),
    )

    try:
        response = requests.put(
            f"{DEVICE_MANAGER_URL}/devices/{name}", data=req.model_dump_json()
        )
        if response.status_code == 200:
            click.echo(response.json())
        else:
            click.echo(
                f"Failed to connect to {DEVICE_MANAGER_URL}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        click.echo(f"Error connecting to {DEVICE_MANAGER_URL}: {e}")


@click.command()
@click.option("--name", prompt="Device name", help="The port of the HTTP server.")
def delete_device(name):
    req = DeleteDeviceRequest(device_id=name)
    try:
        response = requests.delete(
            f"{DEVICE_MANAGER_URL}/devices/{name}", data=req.model_dump_json()
        )
        if response.status_code == 200:
            click.echo(response.json())
        else:
            click.echo(
                f"Failed to disconnect from {DEVICE_MANAGER_URL}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        click.echo(f"Error disconnecting from {DEVICE_MANAGER_URL}: {e}")


@click.command()
@click.option("--name", prompt="Device name", help="The port of the HTTP server.")
@click.option("--command", prompt="Command", help="Command to send.")
def send_command(name, command):
    req = CommandRequest(command=command)
    try:
        response = requests.post(
            f"{DEVICE_MANAGER_URL}/devices/{name}/send_command",
            data=req.model_dump_json(),
        )
        if response.status_code == 200:
            click.echo(response.json())
        else:
            click.echo(
                f"Failed to send command to {DEVICE_MANAGER_URL}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        click.echo(f"Error sending command to {DEVICE_MANAGER_URL}: {e}")
        return


@cli.command()
def get_devices():
    try:
        response = requests.get(f"{DEVICE_MANAGER_URL}/devices")
        if response.status_code == 200:
            click.echo(f"Devices: {response.json()}")
        else:
            click.echo(
                f"Failed to get devices from {DEVICE_MANAGER_URL}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        click.echo(f"Error getting devices from {DEVICE_MANAGER_URL}: {e}")
        return


cli.add_command(register_device)
cli.add_command(delete_device)
cli.add_command(send_command)
cli.add_command(get_devices)

if __name__ == "__main__":
    cli()
