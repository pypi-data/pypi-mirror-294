# flexenvconfig
A common pattern that I use across many of my Python apps/packages/etc is to use configuration classes that fetch my configs from the environment.  Because each project may use different configurations, and different parts of a project (the database, for example) might have specific configurations,
I created this package which provides an abstract class as a base to build flexible environmental configuration objects.

Here is an example:
```python
from flexenvconfig import BaseFlexEnvConfig


class MongoDBConfig(BaseFlexEnvConfig):
    def __init__(self) -> None:
        self.MONGO_DB_NAME = MongoDBConfig.get_env("MONGO_DB_NAME", "testdb")
        self.MONGO_DB_HOST = MongoDBConfig.get_env("MONGO_DB_HOST", "localhost")
        self.MONGO_DB_PORT = int(MongoDBConfig.get_env("MONGO_DB_PORT", "12345"))
        self.MONGO_DB_USERNAME = MongoDBConfig.get_env("MONGO_DB_USERNAME", "mongouser")
        self.MONGO_DB_PASSWORD = MongoDBConfig.get_env("MONGO_DB_PASSWORD", "mongopassword")
        self.OPTIONAL_CONFIG = MongoDBConfig.get_env("OPTIONAL_CONFIG")

    def validate(self) -> bool:
        return all([self.MONGO_DB_NAME, self.MONGO_DB_HOST, self.MONGO_DB_PORT, self.MONGO_DB_USERNAME, self.MONGO_DB_PASSWORD])
```

`BaseFlexEnvConfig`'s constructor defines the configs which gets sourced from the environment when implemented.  When implemented, the `validate` method is used to validate that a config object contains the required values.

## Development
You'll need poetry and Python 3.11+.  Clone the repo and then run `poetry install`

Then you'll need to install the pre-commit hooks: `poetry run pre-commit install`

You can run the test suite using `make test` and you can manually lint the project using `make lint`
