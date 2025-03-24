import click
from fastapi import FastAPI
from models.data import DeviceConfig, JobStatus
from models.http import (
    CommandRequest,
    CommandResponse,
    GetStatusRequest,
    GetStatusResponse,
)
import asyncio
import uuid
import yaml
import sys
from drivers.factory import get_driver
import uvicorn

print("Starting daemon")
print("Args: ", sys.argv)


async def start_worker():
    async def worker():
        while True:
            job_id, command = await queue.get()
            job_status[job_id] = JobStatus(status="in_progress")
            try:
                result = await driver.send_command(command)
                job_status[job_id] = JobStatus(status="done", result=result)
            except Exception as e:
                job_status[job_id] = JobStatus(status="error", error=str(e))
            queue.task_done()

    asyncio.create_task(worker())


app = FastAPI(on_startup=[start_worker])
queue = asyncio.Queue()
job_status: dict[str, JobStatus] = {}


@app.post("/send_command")
async def send_command(req: CommandRequest) -> CommandResponse:
    job_id = str(uuid.uuid4())
    await queue.put((job_id, req.command))
    job_status[job_id] = JobStatus(status="queued")
    return CommandResponse(job_id=job_id)


@app.get("/status/{job_id}")
async def get_status(req: GetStatusRequest) -> GetStatusResponse:
    job_id = req.job_id
    if job_id not in job_status:
        return GetStatusResponse(error="not found")

    return GetStatusResponse(
        status=job_status[job_id].status, result=job_status[job_id].result
    )


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--host", default="127.0.0.1", help="Host to run the server on")
@click.option("--port", default=8000, help="Port to run the server on")
def main(config_file, host, port):
    with open(config_file) as f:
        raw_config = yaml.safe_load(f)
        print(raw_config)
        config = DeviceConfig.model_validate(raw_config)

    global driver
    driver = get_driver(config.type, config.driver_config.model_dump())

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
