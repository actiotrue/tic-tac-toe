<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { Bars3Icon, ChevronDownIcon, XMarkIcon } from "@heroicons/vue/20/solid";
import { ref } from "vue";
import AuthModal from "@/components/auth/AuthModal.vue";
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import { useAuthModal } from "@/composables/useAuthModal";
import { useAuth } from "@/store/auth.store";

const authStore = useAuth();
const { openAuthModal } = useAuthModal();

const isMobileMenuOpen = ref(false);

async function logout() {
  await authStore.logout();
  window.location.reload();
}
</script>

<template>
  <div class="min-h-screen flex flex-col transition-colors duration-300">
    <nav class="sticky top-0 z-50 backdrop-blur-lg border-b shadow-sm border-custom-transparent">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-3">
            <RouterLink to="/" class="text-lg sm:text-xl font-bold">
              Tic Tac Toe
            </RouterLink>
          </div>

          <div class="hidden md:flex items-center space-x-4">
            <ThemeSwitch />
            <template v-if="!authStore.isLoggedIn">
              <button class="cursor-pointer px-3 py-2 text-sm hover:text-gray-400" @click="openAuthModal('login')">
                Log in
              </button>
              <button
                class="cursor-pointer px-3 py-2 text-sm font-medium rounded-lg shadow-md hover:shadow-lg duration-300 transform hover:-translate-y-0.5"
                @click="openAuthModal('signup')"
              >
                Sign up
              </button>
            </template>
            <template v-else>
              <Menu as="div" class="relative inline-block text-left">
                <div>
                  <MenuButton
                    class="cursor-pointer text-white inline-flex w-full justify-center rounded-md px-4 py-2 bg-violet-400 font-bold hover:opacity-90 hover:transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
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
                          to="/profile"
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
                          class="cursor-pointer group flex w-full items-center rounded-md px-2 py-2 text-sm" :class="[
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
          <button class="md:hidden" @click="isMobileMenuOpen = !isMobileMenuOpen">
            <Bars3Icon v-if="!isMobileMenuOpen" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>
        </div>

        <div v-if="isMobileMenuOpen" class="md:hidden mt-4 space-y-3 pb-4">
          <div class="bg-gray-50 dark:bg-gray-800/50 rounded-2xl p-4 border border-gray-100 dark:border-gray-700/50 space-y-1">
            <div class="flex items-center justify-between pb-3 mb-2 border-b border-gray-200 dark:border-gray-700">
              <span class="text-sm font-medium text-gray-500">Настройки</span>
              <ThemeSwitch />
            </div>

            <template v-if="!authStore.isLoggedIn">
              <button
                class="block w-full text-left px-4 py-3 rounded-xl transition-colors active:bg-gray-200 dark:active:bg-gray-700 font-medium"
                @click="openAuthModal('login')"
              >
                Log in
              </button>
              <button
                class="block w-full text-left px-4 py-3 rounded-xl transition-colors active:bg-gray-200 dark:active:bg-gray-700 font-medium"
                @click="openAuthModal('signup')"
              >
                Sign up
              </button>
            </template>

            <template v-else>
              <RouterLink
                to="/profile"
                class="block w-full px-4 py-3 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-medium text-gray-700 dark:text-gray-200"
              >
                Profile
              </RouterLink>
              <button
                class="block w-full text-left px-4 py-3 rounded-xl text-red-500 font-medium active:bg-red-50 dark:active:bg-red-900/20 transition-colors"
                @click="logout"
              >
                Sign out
              </button>
            </template>
          </div>
        </div>
      </div>
    </nav>
    <main class="grow container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <div class="max-w-6xl mx-auto">
        <slot />
      </div>
    </main>
    <footer class="border-t border-custom-transparent">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col container mx-auto px-4 py-6 text-center items-center justify-center space-y-4">
          <p class="text-sm">
            Created with ❤️ by Jud1k
          </p>
          <a
            href="https://github.com/Jud1k/tic-tac-toe"
            target="_blank"
            rel="noopener noreferrer"
            class="hover:text-gray-300 transition-colors"
          >
            <span class="sr-only">GitHub</span>
            <svg class="w-14 h-14" fill="currentColor" viewBox="0 0 24 24">
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
