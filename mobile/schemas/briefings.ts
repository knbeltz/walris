import { z } from 'zod';

export const IndicatorPointSchema = z.object({
  date: z.iso.date(),
  value: z.number(),
});

export const IndicatorSeriesSchema = z.object({
  item_key: z.string(),
  label: z.string(),
  points: z.array(IndicatorPointSchema),
});

export const NewsItemSchema = z.object({
  headline: z.string(),
  source: z.string(),
  summary: z.string(),
  published_at: z.iso.datetime(),
  url: z.url(),
  sentiment: z.number().nullable(),
});

export type NewsItem = z.infer<typeof NewsItemSchema>;

export const UserBriefingResponseSchema = z.object({
  date: z.iso.date(),
  content: z.object({
    headline: z.string(),
    sections: z.array(
      z.object({
        heading: z.string(),
        body: z.string(),
      }),
    ),
  }),
  indicators: z.array(IndicatorSeriesSchema),
  news: z.array(NewsItemSchema),
});

export type UserBriefingResponse = z.infer<typeof UserBriefingResponseSchema>;
