<script lang="ts" setup>
import { useForm } from "vee-validate";
import { ref } from "vue";
import { loginSchema } from "@/schemas/auth";
import { useAuth } from "@/store/auth.store";
import { getErrorMessage } from "@/utils";
import { fieldOptions } from "./utils";

const emit = defineEmits<{ success: [] }>();

const authStore = useAuth();

const apiError = ref<string | null>(null);

const { isSubmitting, errors, defineField, handleSubmit } = useForm({
  validationSchema: loginSchema,
  initialValues: {
    username: "",
    password: "",
  },
  validateOnMount: false,
});

const [username, usernameProps] = defineField("username", fieldOptions);
const [password, passwordProps] = defineField("password", fieldOptions);

const onSubmit = handleSubmit(async (values) => {
  try {
    apiError.value = null;
    await authStore.login(values.username, values.password);
    emit("success");
  }
  catch (err: unknown) {
    apiError.value = getErrorMessage(err);
    console.error(err);
  }
});
</script>

<template>
  <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
    <h1 v-if="apiError" class="text-red-600 p-2 rounded-md">
      {{ apiError }}
    </h1>
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-200">Username</label>
      <input
        v-model="username"
        v-bind="usernameProps"
        type="text"
        placeholder="Enter username"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
        :class="{ 'border-red-500': errors.username }"
      >
      <span v-if="errors.username" class="text-red-500 text-xs mt-1 block">
        {{ errors.username }}
      </span>
    </div>
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-200">Password</label>
      <input
        v-model="password"
        v-bind="passwordProps"
        type="password"
        placeholder="••••••••"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
        :class="{ 'border-red-500': errors.password }"
      >
      <span v-if="errors.password" class="text-red-500 text-xs mt-1 block">
        {{ errors.password }}
      </span>
    </div>
    <button
      type="submit"
      class="cursor-pointer w-full mt-4 py-2 px-4 rounded-md font-medium bg-blue-600 hover:bg-blue-700 text-white transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      :disabled="isSubmitting"
    >
      {{ isSubmitting ? 'Logging in...' : 'Log In' }}
    </button>
  </form>
</template>
