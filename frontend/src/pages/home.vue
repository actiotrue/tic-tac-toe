<script setup lang="ts">
import { GlobeAmericasIcon, PlayIcon, TrophyIcon, UserIcon } from "@heroicons/vue/24/solid";
import { useRouter } from "vue-router";
import GameLeaderboard from "@/components/GameLeaderboard.vue";
import OngoingGames from "@/components/OngoingGames.vue";

import { useAuthModal } from "@/composables/useAuthModal";
import AppLayout from "@/layouts/AppLayout.vue";
import { useAuth } from "@/store/auth.store";

const authStore = useAuth();

const router = useRouter();
const { openAuthModal } = useAuthModal();

function startGame(mode: "pvp" | "pve") {
  router.push({
    path: "game",
    query: { mode },
  });
}
</script>

<template>
  <AppLayout>
    <div class="py-4 sm:py-8">
      <div class="mx-auto w-full max-w-6xl space-y-6 sm:space-y-8">
        <div class="text-center space-y-4">
          <h1 class="text-4xl font-bold sm:text-5xl">
            Tic Tac Toe
          </h1>
          <p class="mx-auto max-w-2xl text-base text-gray-400 sm:text-lg">
            Just tic tac toe. If you don't interesting go away.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mx-auto w-full max-w-2xl">
          <button
            class="flex w-full items-center cursor-pointer justify-center gap-3 rounded-md bg-violet-400 px-4 py-3 text-base text-white sm:px-8 sm:text-lg"
            @click="startGame('pvp')"
          >
            <PlayIcon class="w-6 h-6" />
            <span class="text-center">Play against people</span>
          </button>
          <button
            class="flex w-full items-center justify-center cursor-pointer gap-3 rounded-md bg-violet-400 px-4 py-3 text-base text-white sm:px-8 sm:text-lg"
            @click="startGame('pve')"
          >
            <PlayIcon class="w-6 h-6" />
            <span class="text-center">Play against AI</span>
          </button>
        </div>

        <div class="grid gap-6 md:grid-cols-2 lg:gap-10">
          <div v-if="authStore.isLoggedIn" class="space-y-4">
            <div>
              <div class="flex items-center gap-2 text-lg font-semibold">
                <GlobeAmericasIcon class="w-6 h-6" />
                <span>Ongoing games</span>
              </div>
              <p class="text-gray-400 text-sm">
                See how other players play
              </p>
            </div>

            <div class="rounded-xl bg-gray-800/40 p-4">
              <OngoingGames />
            </div>
          </div>
          <div v-else class="space-y-4">
            <div>
              <div class="flex items-center gap-2 text-lg font-semibold">
                <UserIcon class="w-6 h-6" />
                <span>Create an Account</span>
              </div>
              <p class="text-gray-400 text-sm">
                Track your stats and compete!
              </p>
            </div>

            <div class="rounded-xl bg-gray-800/40 p-4 space-y-4">
              <p>
                Sign up to save your progress, track your wins, and climb the leaderboard!
              </p>

              <button
                class="w-full py-2 rounded-md bg-violet-400 text-white transition hover:bg-violet-500"
                @click="openAuthModal('signup')"
              >
                Get Started
              </button>
            </div>
          </div>

          <div class="space-y-4">
            <div class="flex items-center gap-2 font-semibold text-lg">
              <TrophyIcon class="w-6 h-6 text-yellow-400" />
              <span>Leaderboard</span>
            </div>
            <div class="rounded-xl bg-gray-800/40 p-4">
              <GameLeaderboard />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
