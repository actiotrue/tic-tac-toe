import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const method = ref<"signup" | "login">("login");

export function useAuthModal() {
  const router = useRouter();
  const route = useRoute();

  const openModal = (newMethod: "signup" | "login") => {
    method.value = newMethod;
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        modal: "auth",
      },
    });
  };

  const closeModal = () => {
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        modal: undefined,
      },
    });
  };

  const isOpen = computed(() => {
    return route.query.modal === "auth";
  });

  function toggleMethod() {
    const newMethod = method.value === "login" ? "signup" : "login";
    method.value = newMethod;
  }

  return { isOpen, method, openModal, closeModal, toggleMethod };
}
