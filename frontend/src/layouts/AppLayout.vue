<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { Bars3Icon, ChevronDownIcon, XMarkIcon } from "@heroicons/vue/20/solid";
import { ref } from "vue";
import AuthModal from "@/components/auth/AuthModal.vue";
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import { useAuthModal } from "@/composables/useAuthModal";
import { useAuth } from "@/store/auth.store";

const authStore = useAuth();
const { openModal } = useAuthModal();

const isMobileMenuOpen = ref(false);

async function logout() {
  await authStore.logout();
  window.location.reload();
}
</script>

<template>
  <div class="flex min-h-screen flex-col overflow-x-clip transition-colors duration-300">
    <nav class="sticky top-0 z-50 border-b border-custom-transparent shadow-sm backdrop-blur-lg">
      <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 items-center justify-between gap-3">
          <div class="flex min-w-0 items-center space-x-3">
            <RouterLink to="/" class="truncate text-lg font-bold sm:text-xl">
              Tic Tac Toe
            </RouterLink>
          </div>

          <div class="hidden items-center space-x-4 md:flex">
            <ThemeSwitch />
            <template v-if="!authStore.isLoggedIn">
              <button class="cursor-pointer px-3 py-2 text-sm hover:text-gray-400" @click="openModal('login')">
                Log in
              </button>
              <button
                class="transform cursor-pointer rounded-lg px-3 py-2 text-sm font-medium shadow-md duration-300 hover:-translate-y-0.5 hover:shadow-lg"
                @click="openModal('signup')"
              >
                Sign up
              </button>
            </template>
            <template v-else>
              <Menu as="div" class="relative inline-block text-left">
                <div>
                  <MenuButton
                    class="inline-flex w-full cursor-pointer justify-center rounded-md bg-violet-400 px-4 py-2 font-bold text-white hover:opacity-90 hover:transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
                  >
                    Profile
                    <ChevronDownIcon
                      class="-mr-1 ml-2 h-5 w-5 text-violet-200 hover:text-violet-100"
                      aria-hidden="true"
                    />
                  </MenuButton>
                </div>

                <transition
                  enter-active-class="transition duration-100 ease-out"
                  enter-from-class="transform scale-95 opacity-0"
                  enter-to-class="transform scale-100 opacity-100"
                  leave-active-class="transition duration-75 ease-in"
                  leave-from-class="transform scale-100 opacity-100"
                  leave-to-class="transform scale-95 opacity-0"
                >
                  <MenuItems
                    class="absolute right-0 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none"
                  >
                    <div class="px-1 py-1">
                      <MenuItem v-slot="{ active }">
                        <RouterLink
                          to="/profile/me"
                          class="group flex w-full items-center rounded-md px-2 py-2 text-sm" :class="[
                            active ? 'bg-violet-500 text-white' : 'text-gray-900',
                          ]"
                        >
                          Profile
                        </RouterLink>
                      </MenuItem>
                    </div>
                    <div class="px-1 py-1">
                      <MenuItem v-slot="{ active }">
                        <button
                          class="group flex w-full cursor-pointer items-center rounded-md px-2 py-2 text-sm" :class="[
                            active ? 'bg-violet-500 text-white' : 'text-gray-900',
                          ]"
                          @click="logout"
                        >
                          Sign out
                        </button>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
            </template>
          </div>
          <button class="shrink-0 md:hidden" @click="isMobileMenuOpen = !isMobileMenuOpen">
            <Bars3Icon v-if="!isMobileMenuOpen" class="h-6 w-6" />
            <XMarkIcon v-else class="h-6 w-6" />
          </button>
        </div>

        <div v-if="isMobileMenuOpen" class="mt-4 space-y-3 pb-4 md:hidden">
          <div class="space-y-1 rounded-2xl border border-gray-100 bg-gray-50 p-4 dark:border-gray-700/50 dark:bg-gray-800/50">
            <div class="mb-2 flex items-center justify-between gap-4 border-b border-gray-200 pb-3 dark:border-gray-700">
              <span class="text-sm font-medium">Настройки</span>
              <ThemeSwitch />
            </div>

            <template v-if="!authStore.isLoggedIn">
              <button
                class="block w-full rounded-xl px-4 py-3 text-left font-medium transition-colors active:bg-gray-200 dark:active:bg-gray-700"
                @click="openModal('login')"
              >
                Log in
              </button>
              <button
                class="block w-full rounded-xl px-4 py-3 text-left font-medium transition-colors active:bg-gray-200 dark:active:bg-gray-700"
                @click="openModal('signup')"
              >
                Sign up
              </button>
            </template>

            <template v-else>
              <RouterLink
                to="/profile/me"
                class="block w-full rounded-xl px-4 py-3 font-medium text-gray-700 transition-colors hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
              >
                Profile
              </RouterLink>
              <button
                class="block w-full rounded-xl px-4 py-3 text-left font-medium text-red-500 transition-colors active:bg-red-50 dark:active:bg-red-900/20"
                @click="logout"
              >
                Sign out
              </button>
            </template>
          </div>
        </div>
      </div>
    </nav>
    <main class="grow px-4 py-4">
      <div class="mx-auto w-full max-w-6xl min-w-0">
        <slot />
      </div>
    </main>
    <footer class="border-t border-custom-transparent">
      <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col items-center justify-center space-y-4 px-4 py-6 text-center">
          <p class="text-sm">
            Created with ❤️ by Actiotrue
          </p>
          <a
            href="https://github.com/actiotrue/tic-tac-toe"
            target="_blank"
            rel="noopener noreferrer"
            class="transition-colors hover:text-gray-300"
          >
            <span class="sr-only">GitHub</span>
            <svg class="h-14 w-14" fill="currentColor" viewBox="0 0 24 24">
              <path
                fill-rule="evenodd"
                d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                clip-rule="evenodd"
              />
            </svg>
          </a>
          <span class="text-sm"> Tic Tac Toe © {{ new Date().getFullYear() }} </span>
        </div>
      </div>
    </footer>
    <AuthModal />
  </div>
</template>
