import { z } from "zod";

export const IndicatorPointSchema = z.object({
    date: z.iso.date(),
    value: z.number(),
});

export const IndicatorSeriesSchema = z.object({
    item_key: z.string(),
    label: z.string(),
    points: z.array(IndicatorPointSchema),
});

export const UserBriefingResponseSchema = z.object({
    date: z.iso.date(),
    content: z.object({
        headline: z.string(),
        sections: z.array(
            z.object({
                heading: z.string(),
                body: z.string(),
            })
        ),
    }),
    indicators: z.array(IndicatorSeriesSchema),
});

export type UserBriefingResponse = z.infer<typeof UserBriefingResponseSchema>;
