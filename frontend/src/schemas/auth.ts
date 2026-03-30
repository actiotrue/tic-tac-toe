import { toTypedSchema } from "@vee-validate/zod";
import z from "zod";

export const loginSchema = toTypedSchema(
  z.object({
    username: z.string().min(5).max(20),
    password: z.string().min(8, "Password too short").max(32, "Password too long"),
  }),
);

export const signupSchema = toTypedSchema(
  z
    .object({
      username: z.string().min(5).max(20),
      password: z.string().min(8, "Password too short").max(32, "Password too long"),
      confirmPassword: z.string(),
    })
    .refine(data => data.password === data.confirmPassword, {
      message: "Passwords don't match",
      path: ["confirmPassword"],
    }),
);
