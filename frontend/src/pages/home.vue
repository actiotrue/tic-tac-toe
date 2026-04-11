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
    <div class="container px-2 py-8">
      <div class="max-w-6xl space-y-8">
        <div class="text-center space-y-4">
          <h1 class="text-5xl font-bold">
            Tic Tac Toe
          </h1>
          <p class="text-lg text-gray-400">
            Just tic tac toe. If you don't interesting go away.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mx-auto w-full max-w-2xl">
          <button
            class="cursor-pointer text-white bg-violet-400 w-full rounded-md text-base sm:text-lg px-4 sm:px-8 py-3 flex items-center gap-3 justify-center"
            @click="startGame('pvp')"
          >
            <PlayIcon class="w-6 h-6" />
            Play against people
          </button>
          <button
            class="cursor-pointer text-white bg-violet-400 w-full rounded-md text-base sm:text-lg px-4 sm:px-8 py-3 flex items-center gap-3 justify-center"
            @click="startGame('pve')"
          >
            <PlayIcon class="w-6 h-6" />
            Play against AI
          </button>
        </div>

        <div class="grid md:grid-cols-2 gap-12">
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
