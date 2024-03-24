from pydantic import BaseModel, field_validator


class ChallengeInputModel(BaseModel):
    title: str
    description: str | None = None
    main_metric_parameters: str
    type: str
    main_metric: str
    deadline: str | None = None
    award: str | None = None
    challenge_source: str

    @field_validator("title")
    def title_validator(cls, value: str) -> str:
        """Title field validation."""
        if "dupa" in value:
            raise ValueError("Use proper words for title")

        return value


example1 = ChallengeInputModel(
    title="dupa blada",
    main_metric_parameters="abc",
    type="abc",
    main_metric="abc",
    challenge_source="abc"
)
example2 = ChallengeInputModel(
    title="blada",
    main_metric_parameters="abc",
    type="abc",
    main_metric="abc",
    challenge_source="abc"
)
print(example1)
print(example2)
