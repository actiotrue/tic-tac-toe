<script lang="ts" setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import GameVsAI from "@/components/game/GameVsAI.vue";
import GameSpectator from "@/components/game/GameSpectator.vue";
import GameVsPlayer from "@/components/game/GameVsPlayer.vue";
import AppLayout from "@/layouts/AppLayout.vue";

type GameMode = "pve" | "pvp" | "spectate";

const route = useRoute();

const mode = computed<GameMode>(() => {
  const m = route.query.mode;
  return m === "pvp" || m === "pve" || m === "spectate" ? m : "pve";
});

const gameId = computed<string>(() => {
  const value = route.query.gameId;
  return typeof value === "string" ? value : "";
});
</script>

<template>
  <AppLayout>
    <div class="w-full">
      <GameVsPlayer v-if="mode === 'pvp'" />
      <GameVsAI v-else-if="mode === 'pve'" />
      <GameSpectator v-else :key="gameId" :game-id="gameId" />
    </div>
  </AppLayout>
</template>
