<script lang="ts" setup>
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from "@headlessui/vue";

defineProps<{
  isOpen: boolean;
  isRematch: boolean;
  result: string;
}>();

const emit = defineEmits(["close", "rematch", "newGame", "home"]);
</script>

<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="emit('close')">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-slate-900/80 backdrop-blur-md" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
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
              class="w-full max-w-md transform overflow-hidden rounded-3xl bg-slate-800 border border-slate-700 p-5 sm:p-8 text-center shadow-2xl transition-all"
            >
              <DialogTitle as="h3" class="text-2xl font-black uppercase tracking-wider text-white">
                Game Over
              </DialogTitle>

              <div class="mt-8 flex flex-col sm:flex-row items-center justify-center sm:justify-between gap-6 sm:gap-8">
                <div class="relative flex flex-col items-center gap-3 flex-1">
                  <slot name="player-left" />
                </div>

                <div class="text-xl sm:text-4xl font-black text-slate-600 shrink-0 my-2 sm:my-0">
                  VS
                </div>

                <div class="relative flex flex-col items-center gap-3 flex-1">
                  <slot name="player-right" />
                </div>
              </div>

              <div class="mt-6 mb-8">
                <div class="flex flex-col items-center justify-center gap-2 sm:flex-row">
                  <span class="text-slate-400 font-medium">Result:</span>
                  <p class="break-words text-xl font-bold text-indigo-400">
                    {{ result }}
                  </p>
                </div>
              </div>

              <div class="flex flex-col gap-3">
                <button
                  class="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl
                  transition-colors cursor-pointer disabled:bg-indigo-800 disabled:text-slate-400 disabled:cursor-not-allowed"
                  :disabled="isRematch"
                  @click="emit('rematch')"
                >
                  Rematch
                </button>
                <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  <button class="py-3 px-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition-colors cursor-pointer" @click="emit('newGame')">
                    New Game
                  </button>
                  <button class="py-3 px-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition-colors cursor-pointer" @click="emit('home')">
                    Home
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
