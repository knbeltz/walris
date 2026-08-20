import { z } from "zod";

export const UserPreferencesSchema = z.object({
    category: z.string().nullable(),
    additional_topics: z.array(z.string())
})

export type UserPreferences = z.infer<
    typeof UserPreferencesSchema
>;
