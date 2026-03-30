<script lang="ts" setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import GameVsAI from "@/components/game/GameVsAI.vue";
import GameVsPlayer from "@/components/game/GameVsPlayer.vue";
import AppLayout from "@/layouts/AppLayout.vue";

type GameMode = "pve" | "pvp";

const route = useRoute();

const mode = computed<GameMode>(() => {
  const m = route.query.mode;
  return m === "pvp" || m === "pve" ? m : "pve";
});
</script>

<template>
  <AppLayout>
    <div class="container">
      <GameVsPlayer v-if="mode === 'pvp'" />
      <GameVsAI v-else />
    </div>
  </AppLayout>
</template>
