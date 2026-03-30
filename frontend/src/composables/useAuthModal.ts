import { useRouter } from "vue-router";

export function useAuthModal() {
  const router = useRouter();

  const openAuthModal = (method: "signup" | "login" = "signup") => {
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        modal: "auth",
        method,
      },
    });
  };

  return { openAuthModal };
}
