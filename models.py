import enum
import pathlib
import statistics
from typing import List
from functools import cached_property

from pydantic import Field, BaseModel, ConfigDict, field_validator

from description import dummy_fetch_description as fetch_description


PROMPTS_DIR = pathlib.Path(__file__).parent / "prompts"
SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.txt"
LONG_HAIR_PROMPT_FILE = PROMPTS_DIR / "the_value_of_long_hair.txt"
SHORT_TAIL_PROMPT_FILE = PROMPTS_DIR / "the_value_of_short_hair.txt"


class SurveyResult(BaseModel):
    question_value: int = Field(ge=1, le=7)
    question_number: int = Field(ge=1, le=10)

    model_config = ConfigDict(strict=True)


class Payload(BaseModel):
    user_id: str = Field(min_length=5)
    survey_results: List[SurveyResult] = Field(max_length=10, min_length=10)

    model_config = ConfigDict(strict=True)

    @field_validator("survey_results")
    def ensure_unique_questions(cls, values: List[SurveyResult]) -> List[SurveyResult]:  # noqa
        question_numbers = {result.question_number for result in values}

        if len(question_numbers) != 10:
            raise ValueError("Question numbers must be unique values between 1 and 10")

        # sort so that it's easier to access
        return sorted(values, key=lambda result: result.question_number)

    # ---- convenience methods ----

    def qvalue(self, question_number: int) -> int:
        """
        Convenience method to get the value of a question
        """
        # Wanna be pedantic? Uncomment the line below. It'll work.
        # assert self.survey_results[question_number - 1].question_number == question_number
        return self.survey_results[question_number - 1].question_value

    @cached_property
    def average_value(self) -> float:
        return statistics.mean(result.question_value for result in self.survey_results)


class Insights(BaseModel):

    class CatDog(str, enum.Enum):
        cats = "cats"
        dogs = "dogs"

    class OverallAnalysis(str, enum.Enum):
        unsure = "unsure"
        certain = "certain"

    class LongShort(str, enum.Enum):
        """Don't even bother trying to understand the naming convention."""

        long = "long"
        short = "short"

    cat_dog: CatDog
    description: str
    fur_value: LongShort
    tail_value: LongShort
    overall_analysis: OverallAnalysis

    @classmethod
    async def from_payload(cls, payload: Payload) -> "Insights":

        cat_dog = cls.CatDog.cats if payload.qvalue(10) > 5 >= payload.qvalue(9) else cls.CatDog.dogs

        fur_value = cls.LongShort.long if payload.average_value > 5 else cls.LongShort.short

        tail_value = cls.LongShort.long if payload.qvalue(7) > 4 else cls.LongShort.short

        overall_analysis = (
            cls.OverallAnalysis.unsure
            if (payload.qvalue(1) == 7) and (payload.qvalue(4) < 3)
            else cls.OverallAnalysis.certain
        )

        system_prompt = SYSTEM_PROMPT_FILE.read_text()
        prompt = SHORT_TAIL_PROMPT_FILE.read_text() if payload.average_value > 4 else LONG_HAIR_PROMPT_FILE.read_text()
        description = await fetch_description(prompt, system_prompt)

        return cls(
            cat_dog=cat_dog,
            fur_value=fur_value,
            tail_value=tail_value,
            description=description,
            overall_analysis=overall_analysis,
        )


class Statistics(BaseModel):

    mean: float
    median: float
    std_dev: float

    @classmethod
    def from_payload(cls, payload: Payload) -> "Statistics":
        return cls(
            mean=payload.average_value,
            median=statistics.median(result.question_value for result in payload.survey_results),
            std_dev=statistics.stdev(result.question_value for result in payload.survey_results),
        )


class StatisticsQuery(BaseModel):
    user_id: str

    model_config = ConfigDict(strict=True)
