import { toTypedSchema } from "@vee-validate/zod";
import { z } from "zod";

export const updateUsernameSchema = toTypedSchema(
  z.object({
    username: z.string().min(5, "Username too short").max(20, "Username too long"),
  }),
);
