# pg-async-events

A simple asynchronous event handling library using PostgreSQL notifications. This library allows you to subscribe to and publish events using PostgreSQL's `LISTEN/NOTIFY` mechanism in an asynchronous environment.

This is useful in generative AI applications or for situations where other pub/sub systems are overkill.

## Features

- **Asynchronous Event Handling:** Leverage `asyncio` and `asyncpg` to handle events without blocking your main application logic.
- **PostgreSQL Notifications:** Seamlessly integrates with PostgreSQL's `LISTEN/NOTIFY` to provide real-time event notifications.
- **Simple API:** Easy-to-use API for subscribing to channels and notifying events.

## Installation

You can install the package directly from PyPI:

```bash
pip install pg_async_events
```

## Usage

### Quart

```python
import asyncpg
import pg_async_events as events

# Add your postgres credentials from the env
db_config = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "min_size": 1,
    "max_size": 5,
}

@app.before_serving
async def setup():
    pool = await asyncpg.create_pool(**db_config)
    await events.initialize(pool)
```


## Notifications

```python
import pg_async_events as events

async def listen_to_events():
    async for message in events.subscribe('your_channel'):
        print('Received:', message)

async def publish_event():
    payload = {'key': 'value'}
    await events.notify('your_channel', payload)
```

## Requirements
- Python 3.8+
- PostgreSQL 9.0+ (with support for LISTEN/NOTIFY)
- asyncpg library

## Author

Built by [255labs.xyz](https://255labs.xyz), the AI product and consulting startup helping people adapt to the AI age with consulting, product, and open-source development.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss the changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Thanks

* asyncpg for providing the asynchronous PostgreSQL driver.
* PostgreSQL community for their robust database and features like LISTEN/NOTIFY.

