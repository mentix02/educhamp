import { z } from "zod";

const QuestionValueSchema = z.coerce.number().int().min(1).max(7);

export const questionValuesSchema = z.array(QuestionValueSchema).length(10);

export const SurveyResultSchema = z.object({
  question_value: QuestionValueSchema,
  question_number: z.number().int().min(1).max(10),
});

export const PayloadSchema = z.object({
  user_id: z.string(),
  survey_results: z.array(SurveyResultSchema).length(10),
});

type LongShort = "long" | "short";

export type InsightResponse = {
  readonly description: string;
  readonly fur_value: LongShort;
  readonly tail_value: LongShort;
  readonly cat_dog: "cats" | "dogs";
  readonly overall_analysis: "unsure" | "certain";
};

export type StatsResponse = {
  readonly mean: number;
  readonly median: number;
  readonly std_dev: number;
};

export type Payload = z.infer<typeof PayloadSchema>;
export type SurveyResult = z.infer<typeof SurveyResultSchema>;
