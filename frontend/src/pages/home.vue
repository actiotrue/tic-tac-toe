<script setup lang="ts">
import { GlobeAmericasIcon, PlayIcon, TrophyIcon, UserIcon } from "@heroicons/vue/24/solid";
import { useRouter } from "vue-router";
import Leaderboard from "@/components/Leaderboard.vue";
import {
  CardContainer,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
            class="flex w-full items-center justify-center gap-3 rounded-md bg-violet-400 px-4 py-3 text-base text-white sm:px-8 sm:text-lg"
            @click="startGame('pvp')"
          >
            <PlayIcon class="w-6 h-6" />
            <span class="text-center">Play against people</span>
          </button>
          <button
            class="flex w-full items-center justify-center gap-3 rounded-md bg-violet-400 px-4 py-3 text-base text-white sm:px-8 sm:text-lg"
            @click="startGame('pve')"
          >
            <PlayIcon class="w-6 h-6" />
            <span class="text-center">Play against AI</span>
          </button>
        </div>

        <div class="grid gap-6 md:grid-cols-2 lg:gap-10">
          <CardContainer v-if="authStore.isLoggedIn">
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <GlobeAmericasIcon class="w-6 h-6" />
                Ongoing games
              </CardTitle>
              <CardDescription>
                <p class="text-gray-400">
                  See how other players play
                </p>
              </CardDescription>
            </CardHeader>
            <CardContent />
            <!-- <OngoingGames /> -->
          </CardContainer>
          <CardContainer v-else>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <UserIcon class="w-6 h-6" />
                <h3 class="font-semibold">
                  Create an Account
                </h3>
              </CardTitle>
              <CardDescription>Track your stats and compete!</CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <p class="text-gray-400">
                Sign up to save your progress, track your wins, and climb the leaderboard!
              </p>
              <button
                class="cursor-pointer text-white w-full py-2 rounded-md items-center bg-violet-400 justify-center"
                @click="openAuthModal('signup')"
              >
                Get Started
              </button>
            </CardContent>
          </CardContainer>

          <CardContainer>
            <CardHeader>
              <CardTitle class="flex items-center gap-2 font-semibold">
                <TrophyIcon class="w-6 h-6 text-yellow-400" />Leaderboard
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Leaderboard />
            </CardContent>
          </CardContainer>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
