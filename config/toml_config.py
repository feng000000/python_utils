from typing import Type
from typing import Tuple
from typing import List
from typing import Dict

from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import TomlConfigSettingsSource


class Table(BaseModel):
    table_field1: str
    table_field2: List[int]
    table_field3: Dict[str, str]
    dict_on_list: List[Dict]

class Settings(BaseSettings):

    name: str
    age: int
    height: float
    employed: bool
    dob: datetime
    dob_utc8: datetime

    table_name: Table



    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls, "./config/config.toml"),)


settings = Settings()  # type: ignore


if __name__ == "__main__":
    print(settings.name)
    print(settings.age)
    print(settings.height)
    print(settings.dob)
    print(settings.dob_utc8)

    print(settings.table_name.table_field1)
    print(settings.table_name.table_field2)
    print(settings.table_name.table_field3)
    print(settings.table_name.dict_on_list)