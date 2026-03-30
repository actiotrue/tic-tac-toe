import { isAxiosError } from "axios";

export function getErrorMessage(error: unknown): string {
  if (isAxiosError(error)) {
    return error.response?.data?.detail || "Server error";
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Unknown error";
}

export function formatDate(date: string | Date) {
  const dateObj = new Date(date);
  return dateObj.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}
