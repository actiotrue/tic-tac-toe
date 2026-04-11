<script lang="ts" setup>
import type { GameBoard, PlayerSymbol, Winner } from "../../types/game";
import { CardContainer, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

const props = defineProps<{
  board: GameBoard;
  currentPlayer: PlayerSymbol | null;
  winner: Winner | null;
  winningLine?: number[];
  disabled?: boolean;
  statusMessage: string;
}>();

const emit = defineEmits<{
  cellClick: [index: number];
}>();
</script>

<template>
  <div class="mx-auto flex w-full max-w-2xl flex-col space-y-4 sm:space-y-6">
    <CardContainer class="w-full">
      <CardHeader>
        <CardTitle class="break-words text-center text-xl font-bold sm:text-2xl">
          {{ statusMessage }}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="mx-auto grid aspect-square w-full max-w-[min(100%,24rem)] grid-cols-3 gap-2 sm:gap-3">
          <button
            v-for="(cell, index) in board"
            :key="index"
            class="flex aspect-square items-center justify-center rounded-lg bg-gray-200 text-3xl font-bold sm:text-5xl"
            :disabled="!!cell || !!props.winner || disabled"
            :class="[
              cell === 'X' ? 'text-blue-600' : 'text-red-600',
              props.winningLine?.includes(index) ? 'bg-green-400' : 'bg-gray-200',
              {
                'cursor-pointer hover:opacity-80 active:scale-95 transition-all':
                  !cell && !props.winner && !disabled,
                'cursor-not-allowed': disabled && !props.winner,
              },
            ]"
            @click="emit('cellClick', index)"
          >
            <Transition name="pop" mode="out-in">
              <span :key="cell ? cell : 'empty'">
                {{ cell }}
              </span>
            </Transition>
          </button>
        </div>
      </CardContent>
      <CardFooter v-if="$slots.footer">
        <slot name="footer" />
      </CardFooter>
    </CardContainer>
  </div>
</template>

<style scoped>
.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.5) rotate(-10deg);
}

.pop-enter-active,
.pop-leave-active {
  transition: all 0.08s ease-out;
}

.pop-enter-to,
.pop-leave-from {
  opacity: 1;
  transform: scale(1) rotate(0deg);
}
</style>
