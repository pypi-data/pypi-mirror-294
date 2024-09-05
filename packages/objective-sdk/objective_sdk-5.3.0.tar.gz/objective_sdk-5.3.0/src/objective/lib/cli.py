import json
import asyncio

import click
import aiofiles
from tqdm import tqdm

from objective import AsyncObjective


@click.group()
def cli():
    pass

@cli.command()
@click.argument('file_path')
@click.option('--id-field', help='Field to use as object ID for PUT operations')
@click.option('--max-concurrency', default=32, help='Maximum number of concurrent tasks')
@click.option('--batch-size', default=512, help='Number of operations per batch')
def upsert_file(file_path, id_field, max_concurrency, batch_size):
    """Batch upsert all rows in the given JSONL file."""
    asyncio.run(async_upsert_file(file_path, id_field, max_concurrency, batch_size))

async def async_upsert_file(file_path, id_field, max_concurrency, batch_size):
    async with AsyncObjective() as client:
        async def process_line(line):
            obj = json.loads(line)
            if id_field:
                if id_field not in obj:
                    click.echo(f"Error: ID field '{id_field}' not found in object: {obj}", err=True)
                    return None
                return {
                    "method": "PUT",
                    "object": obj,
                    "object_id": obj[id_field]
                }
            else:
                return {
                    "method": "POST",
                    "object": obj
                }

        async def process_batch(batch):
            operations = [op for op in batch if op is not None]
            if operations:
                await client.objects.batch(operations=operations)
            return len(operations)

        async def read_and_process():
            operations = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    operation = await process_line(line)
                    if operation:
                        operations.append(operation)
                        if len(operations) >= batch_size:
                            yield operations
                            operations = []
                if operations:
                    yield operations

        total_operations = 0
        pbar = tqdm(total=total_operations, desc="Processing operations")

        semaphore = asyncio.Semaphore(max_concurrency)
        async def process_with_semaphore(batch, semaphore):
            async with semaphore:
                processed = await process_batch(batch)
                pbar.update(processed)

        tasks = []

        async for batch in read_and_process():
            tasks.append(asyncio.create_task(process_with_semaphore(batch, semaphore)))
            total_operations += len(batch)
            pbar.total = total_operations  # Update the total count
            pbar.refresh()  # Refresh the progress bar


        await asyncio.gather(*tasks)
        pbar.close()
        click.echo("All operations processed.")

if __name__ == '__main__':
    cli()