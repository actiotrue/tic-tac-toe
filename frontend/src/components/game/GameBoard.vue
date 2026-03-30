<script lang="ts" setup>
import type { GameBoard, PlayerSymbol, Winner } from "../../types/game";
import { CardContainer, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

const props = defineProps<{
  board: GameBoard;
  currentPlayer: PlayerSymbol;
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
  <div class="flex flex-col max-w-2xl mx-auto space-y-6">
    <h1 class="font-semibold text-2xl text-center">
      Game board
    </h1>
    <CardContainer class="w-full">
      <CardHeader>
        <CardTitle class="text-center text-2xl font-bold">
          {{ statusMessage }}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-3 gap-3 max-w-md mx-auto aspect-square">
          <button
            v-for="(cell, index) in board"
            :key="index"
            class="aspect-square bg-gray-200 rounded-lg text-5xl font-bold flex items-center justify-center"
            :disabled="!!cell || !!props.winner || disabled"
            :class="[
              cell === 'X' ? 'text-blue-600' : 'text-red-600',
              props.winningLine?.includes(index) ? 'bg-green-400' : 'bg-gray-200',
              {
                'cursor-pointer hover:opacity-80 transition-all':
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
