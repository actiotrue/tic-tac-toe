<script setup lang="ts">
import { PencilIcon } from "@heroicons/vue/24/outline";
import { useForm } from "vee-validate";
import { nextTick, ref } from "vue";
import { updateUsernameSchema } from "@/schemas/profile";

const props = defineProps<{ username: string; loading: boolean }>();

const emits = defineEmits<{
  (e: "update", username: string): void;
}>();

const { errors, handleSubmit, defineField, setFieldValue } = useForm({
  validationSchema: updateUsernameSchema,
  initialValues: {
    username: props.username,
  },
});

const isEditing = ref<boolean>(false);
const usernameInput = ref<HTMLInputElement | null>(null);
const [newUsername, newUsernameProps] = defineField("username", {
  validateOnBlur: false,
  validateOnChange: false,
  validateOnInput: false,
  validateOnModelUpdate: false,
});

async function startEditing() {
  setFieldValue("username", props.username);
  isEditing.value = true;
  await nextTick();
  usernameInput.value?.focus();
}

const onSubmit = handleSubmit(async (values) => {
  if (!newUsername || values.username === props.username) {
    isEditing.value = false;
    return;
  }
  const trimmedName = values.username.trim();
  if (trimmedName && trimmedName !== props.username) {
    emits("update", trimmedName);
  }
  isEditing.value = false;
});

function onBlur() {
  if (!props.loading) {
    isEditing.value = false;
  }
}
</script>

<template>
  <div class="flex items-center gap-3 mb-2 md:justify-start">
    <template v-if="!isEditing">
      <h1 class="text-3xl font-bold">
        {{ props.username }}
      </h1>
      <button
        class="text-gray-400 hover:text-white transition cursor-pointer"
        @click="startEditing"
      >
        <PencilIcon class="w-5 h-5" />
      </button>
    </template>

    <form v-else class="items-center gap-3" @submit.prevent="onSubmit">
      <span v-if="errors.username" class="text-red-500 text-sm mb-1 block">
        {{ errors.username }}
      </span>
      <input
        ref="usernameInput"
        v-model="newUsername"
        v-bind="newUsernameProps"
        type="text"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white"
        :disabled="props.loading"
        @keyup.esc="isEditing = false"
        @blur="onBlur"
      >
    </form>
  </div>
</template>
