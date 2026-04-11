<script setup lang="ts">
import type { RankedPlayer } from "@/types/player";
import {
  CalendarIcon,
  ClipboardDocumentIcon,
  SparklesIcon,
  TrophyIcon,
} from "@heroicons/vue/24/outline";
import { onMounted, ref } from "vue";
import { toast } from "vue3-toastify";
import { getPlayerWithRank, updatePlayer } from "@/api/player";
import { deleteFromCloudinary, uploadToCloudinary } from "@/cloudinary";
import EditableUsername from "@/components/profile/EditableUsername.vue";
import ProfileAvatar from "@/components/profile/ProfileAvatar.vue";
import RecentGames from "@/components/profile/RecentGames.vue";
import StatisticChart from "@/components/profile/StatisticChart.vue";
import { CardContainer, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import AppLayout from "@/layouts/AppLayout.vue";
import { formatDate, getErrorMessage } from "@/utils";

const isLoading = ref<boolean>(false);
const currentPlayer = ref<RankedPlayer | null>(null);

async function fetchPlayer() {
  try {
    isLoading.value = true;
    const player = await getPlayerWithRank();
    currentPlayer.value = player;
  }
  finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await fetchPlayer();
});

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
          <LoadingSpinner v-if="isLoading" size="sm" />
          <ProfileAvatar
            v-else-if="currentPlayer"
            :image-url="currentPlayer.imageUrl"
            @update="updateAvatar"
          />
          <div class="min-w-0 flex-1 text-center md:text-left">
            <div>
              <LoadingSpinner v-if="isLoading" size="sm" />
              <EditableUsername
                v-else-if="currentPlayer"
                :username="currentPlayer.username"
                :loading="isLoading"
                @update="updateUsername"
              />
            </div>
            <div class="flex flex-wrap justify-center gap-4 md:justify-start">
              <LoadingSpinner v-if="isLoading" size="sm" />
              <div v-else class="flex flex-col items-center gap-2 sm:gap-4 md:items-start lg:flex-row">
                <div class="flex items-center gap-2 text-center md:text-left">
                  <CalendarIcon class="w-4 h-4 text-gray-400" />
                  <span class="break-words text-gray-400">Joined {{ currentPlayer ? formatDate(currentPlayer.createdAt) : '' }}</span>
                </div>
                <div class="flex items-center gap-2 text-center md:text-left">
                  <TrophyIcon class="w-4 h-4 text-yellow-400" />
                  <span class="break-words text-gray-400">Rank: {{ currentPlayer?.rank || 'Failed to load rank' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContainer>

      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <CardContainer>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <ClipboardDocumentIcon class="w-6 h-6" /> Recent Games
              </CardTitle>
            </CardHeader>
            <CardContent>
              <RecentGames />
            </CardContent>
          </CardContainer>
        </div>

        <div class="space-y-6">
          <CardContainer>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <SparklesIcon class="w-6 h-6" /> Game Distribution
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div class="mx-auto flex w-full max-w-xs items-center justify-center">
                <StatisticChart
                  v-if="!isLoading && currentPlayer"
                  :wins="currentPlayer.wins"
                  :draws="currentPlayer.draws"
                  :losses="currentPlayer.losses"
                />
                <LoadingSpinner v-else-if="isLoading" size="md" />
              </div>
            </CardContent>
          </CardContainer>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
