import { Payload, SurveyResult, InsightResponse, StatsResponse, questionValuesSchema } from "./types/survey.ts";

const statsEndpoint = "/stats";
const surveyEndpoint = "/process-survey";

export const submitSurvey = async (user_id: string, question_vals: string[]): Promise<InsightResponse> => {
  const result = await questionValuesSchema.safeParseAsync(question_vals);

  if (!result.success)
    throw new Error("Invalid questions. Please make sure each question value is a number between 1 and 7.");

  const payload: Payload = {
    user_id: user_id,
    survey_results: result.data.map(
      (value, index): SurveyResult => ({ question_value: value, question_number: index + 1 }),
    ),
  };

  const resp = await fetch(surveyEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!resp.ok) {
    const errJson = await resp.json();
    throw new Error(errJson.message);
  }

  return await resp.json();
};

export const fetchStats = async (user_id: string): Promise<StatsResponse> => {
  const query = new URLSearchParams({ user_id });
  const resp = await fetch(`${statsEndpoint}?${query}`);

  if (!resp.ok) {
    const errJson = await resp.json();
    throw new Error(errJson.message);
  }

  return await resp.json();
};
