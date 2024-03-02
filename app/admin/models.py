from pydantic import BaseModel

class UserSettingsModel(BaseModel):
    title: str
    description: str | None = None
    type: str
    main_metric: str
    deadline: str | None = None
    award: str | None = None
    challenge_source: str