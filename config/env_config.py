from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class _BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/.env")


class LogSettings(_BasicSettings):
    LOG_LEVEL: str = Field(...)
    LOG_FILE_PATH: str = Field(...)


class SomeSettings(_BasicSettings):
    LIST_SEPARATED_BY_COMMAS: str = Field(...)

    # 使用 @validator 装饰器解析
    @field_validator("LIST_SEPARATED_BY_COMMAS")
    @classmethod
    def parse_warning_group_members(cls, value: str) -> str:
        res_list = value.replace(" ", "").split(",")
        [int(item) for item in res_list if res_list != ""]
        return value

    @property
    def THE_LIST(self):
        res_list = self.LIST_SEPARATED_BY_COMMAS.replace(" ", "").split(",")
        return [int(item) for item in res_list if res_list != ""]


class Settings(
    LogSettings,
    SomeSettings,
): ...


settings = Settings()  # type: ignore

if __name__ == "__main__":
    print(settings.THE_LIST)