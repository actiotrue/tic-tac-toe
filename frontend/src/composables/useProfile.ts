import { useRouter } from "vue-router";

import { useAuth } from "@/store/auth.store";

export function useProfile() {
  const authStore = useAuth();
  const router = useRouter();

  const goToProfile = (userId: string | undefined) => {
    if (!userId) {
      return;
    }
    if (userId === authStore.userId) {
      router.push({ name: "profile-me" });
    }
    else {
      router.push({
        name: "profile-user",
        params: { userId },
      });
    }
  };

  return {
    goToProfile,
  };
}
