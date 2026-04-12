<script setup lang="ts">
import type { RankedPlayer } from "@/types/player";
import {
  CalendarIcon,
  ClipboardDocumentIcon,
  SparklesIcon,
  TrophyIcon,
} from "@heroicons/vue/24/outline";
import { computed, ref, watch } from "vue";
import { toast } from "vue3-toastify";
import { useRoute } from "vue-router";
import { getMeWithRank, getPlayerWithRank, updatePlayer } from "@/api/player";
import { deleteFromCloudinary, uploadToCloudinary } from "@/cloudinary";
import AvatarImage from "@/components/AvatarImage.vue";
import EditableUsername from "@/components/profile/EditableUsername.vue";
import ProfileAvatar from "@/components/profile/ProfileAvatar.vue";
import RecentGames from "@/components/profile/RecentGames.vue";
import StatisticChart from "@/components/profile/StatisticChart.vue";
import { CardContainer } from "@/components/ui/card";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import AppLayout from "@/layouts/AppLayout.vue";
import { formatDate, getErrorMessage } from "@/utils";

const route = useRoute();

const isLoading = ref<boolean>(false);
const currentPlayer = ref<RankedPlayer | null>(null);

const isMeRoute = computed(() => route.name === "profile-me");
const userId = computed(() => {
  if (isMeRoute.value)
    return undefined;
  return route.params.userId as string | undefined;
});

async function fetchPlayer() {
  try {
    isLoading.value = true;

    const player = userId.value
      ? await getPlayerWithRank(userId.value)
      : await getMeWithRank();

    currentPlayer.value = player;
  }
  finally {
    isLoading.value = false;
  }
}

watch(
  () => route.fullPath,
  async () => {
    await fetchPlayer();
  },
  { immediate: true },
);

async function updateAvatar(file: File) {
  isLoading.value = true;
  let uploadedImageUrl: string | null = null;
  try {
    uploadedImageUrl = await uploadToCloudinary(file);
    try {
      const updatedPlayer = await updatePlayer({ imageUrl: uploadedImageUrl });
      if (updatedPlayer.imageUrl !== uploadedImageUrl) {
        throw new Error("Failed to update avatar in database");
      }
      if (currentPlayer.value) {
        const rank = currentPlayer.value.rank;
        currentPlayer.value = { ...updatedPlayer, rank };
      }
    }
    catch (err) {
      if (uploadedImageUrl) {
        await deleteFromCloudinary(uploadedImageUrl).catch((err) => {
          console.error(err);
        });
      }
      throw err;
    }
    toast.success("Avatar updated successfully");
  }
  catch (err) {
    toast.error(getErrorMessage(err));
  }
  finally {
    isLoading.value = false;
  }
}

async function updateUsername(newUsername: string) {
  isLoading.value = true;
  try {
    if (!currentPlayer.value)
      return;
    const newPlayer = await updatePlayer({ username: newUsername });
    const rank = currentPlayer?.value.rank;
    currentPlayer.value = { ...newPlayer, rank };
    toast.success("Username updated successfully");
  }
  catch (err) {
    toast.error(getErrorMessage(err));
  }
  finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <div class="py-4 sm:py-8">
      <CardContainer class="mb-8">
        <div class="flex flex-col items-center gap-6 p-1 sm:p-2 md:flex-row">
          <div v-if="isMeRoute">
            <LoadingSpinner v-if="isLoading" size="sm" />
            <ProfileAvatar
              v-else-if="currentPlayer"
              :image-url="currentPlayer.imageUrl"
              @update="updateAvatar"
            />
          </div>
          <div v-else>
            <LoadingSpinner v-if="isLoading" size="sm" />
            <AvatarImage v-else-if="currentPlayer" :image-url="currentPlayer.imageUrl" :width="130" :height="130" />
          </div>
          <div class="min-w-0 flex-1 text-center md:text-left">
            <div>
              <div v-if="isMeRoute">
                <LoadingSpinner v-if="isLoading" size="sm" />
                <EditableUsername
                  v-else-if="currentPlayer"
                  :username="currentPlayer.username"
                  :loading="isLoading"
                  class="mb-2"
                  @update="updateUsername"
                />
              </div>
              <div v-else>
                <LoadingSpinner v-if="isLoading" size="sm" />
                <h1 v-else-if="currentPlayer" class="break-all text-2xl font-bold sm:text-3xl mb-2">
                  {{ currentPlayer.username }}
                </h1>
              </div>
            </div>
            <div class="flex flex-wrap justify-center gap-4 md:justify-start">
              <LoadingSpinner v-if="isLoading" size="sm" />
              <div v-else class="flex flex-col items-center gap-2 sm:gap-4 md:items-start lg:flex-row">
                <div class="flex items-center gap-2 text-center md:text-left">
                  <CalendarIcon class="w-4 h-4 text-gray-400" />
                  <span class="wrap-break-word text-gray-400">Joined {{ currentPlayer ? formatDate(currentPlayer.createdAt) : '' }}</span>
                </div>
                <div class="flex items-center gap-2 text-center md:text-left">
                  <TrophyIcon class="w-4 h-4 text-yellow-400" />
                  <span class="wrap-break-word text-gray-400">Rank: {{ currentPlayer?.rank || 'Failed to load rank' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContainer>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 md:col-span-3 space-y-6">
          <div class="max-w-3xl w-full">
            <div class="flex items-center gap-2 mb-7">
              <ClipboardDocumentIcon class="w-6 h-6" /> Recent Games
            </div>
            <LoadingSpinner v-if="isLoading" size="sm" />
            <RecentGames v-else-if="currentPlayer" :user-id="currentPlayer.userId" />
            <div v-else class="flex items-center justify-center py-4">
              Loading error
            </div>
          </div>
        </div>
        <div class="space-y-6 order-first lg:order-0">
          <div class="flex items-center gap-2">
            <SparklesIcon class="w-6 h-6" /> Game Distribution
          </div>
          <div class="">
            <div class="mx-auto flex w-full items-center justify-center">
              <StatisticChart
                v-if="!isLoading && currentPlayer"
                :wins="currentPlayer.wins"
                :draws="currentPlayer.draws"
                :losses="currentPlayer.losses"
              />
              <LoadingSpinner v-else-if="isLoading" size="md" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
