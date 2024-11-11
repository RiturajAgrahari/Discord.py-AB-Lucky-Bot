from tortoise import Tortoise

from dotenv import load_dotenv
import os

load_dotenv()


async def db_init():
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": os.getenv("DATABASE"),
                        "host": os.getenv("HOST"),
                        "port": os.getenv("PORT"),
                        "password": os.getenv("PASSWORD"),
                        "user": os.getenv("DB_USER"),
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default"
                }
            }
        }
    )

    await Tortoise.generate_schemas(safe=True)
