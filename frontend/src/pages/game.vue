<script lang="ts" setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import GameSpectator from "@/components/game/GameSpectator.vue";
import GameVsAI from "@/components/game/GameVsAI.vue";
import GameVsPlayer from "@/components/game/GameVsPlayer.vue";
import AppLayout from "@/layouts/AppLayout.vue";

type GameMode = "ai" | "player" | "spectate";

const route = useRoute();

const mode = computed<GameMode>(() => {
  if (route.path.includes("player"))
    return "player";
  if (route.path.includes("spectate"))
    return "spectate";
  return "ai";
});

const gameId = computed<string>(() => {
  const value = route.query.gameId;
  return typeof value === "string" ? value : "";
});
</script>

<template>
  <AppLayout>
    <div class="w-full">
      <GameVsPlayer v-if="mode === 'player'" />
      <GameVsAI v-else-if="mode === 'ai'" />
      <GameSpectator v-else-if="mode === 'spectate'" :key="gameId" :game-id="gameId" />
    </div>
  </AppLayout>
</template>
