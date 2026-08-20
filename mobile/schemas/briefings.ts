import { z } from "zod";

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
});

export type UserBriefingResponse = z.infer<
    typeof UserBriefingResponseSchema
>;
