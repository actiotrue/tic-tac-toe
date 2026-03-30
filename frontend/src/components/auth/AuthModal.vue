<script lang="ts" setup>
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from "@headlessui/vue";
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import LoginForm from "./LoginForm.vue";
import SignupForm from "./SignupForm.vue";

const route = useRoute();
const router = useRouter();

const method = computed(() => {
  const m = route.query.method?.toString();
  return m === "signup" ? "signup" : "login";
});

const isOpen = computed(() => {
  return route.query.modal === "auth";
});

function closeModal() {
  router.replace({
    query: {
      ...route.query,
      modal: undefined,
      method: undefined,
    },
  });
}

function toggleMode() {
  const newMethod = method.value === "login" ? "signup" : "login";
  router.replace({
    query: {
      ...route.query,
      method: newMethod,
    },
  });
}

function handleAuthSuccess() {
  closeModal();
}
</script>

<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-white"
              >
                {{ method === 'login' ? 'Log In' : 'Sign Up' }}
              </DialogTitle>

              <div class="mt-4">
                <slot v-if="$slots.default" />
                <SignupForm v-else-if="method === 'signup'" @success="handleAuthSuccess" />
                <LoginForm v-else-if="method === 'login'" @success="handleAuthSuccess" />
              </div>

              <div class="mt-6 flex justify-between items-center">
                <button
                  type="button"
                  class="cursor-pointer text-sm hover:underline text-white"
                  @click="toggleMode"
                >
                  {{ method === 'login' ? 'Need an account?' : 'Already have an account?' }}
                </button>

                <button
                  type="button"
                  class="cursor-pointer rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="closeModal"
                >
                  Close
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
