<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import AuthModal from "@/components/auth/AuthModal.vue";
import { useAuthModal } from "@/composables/useAuthModal";
import { useAuth } from "@/store/auth.store";
import { useTheme } from "@/store/theme.store";

const themeStore = useTheme();
const authStore = useAuth();
const { openAuthModal } = useAuthModal();

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
            <RouterLink
              to="/"
              class="flex items-center space-x-3 hover:opacity-80 transition-opacity"
            >
              <picture>
                <source srcset="/logo.svg" media="(prefer-color-scheme: dark)">
                <img src="/logo.svg" alt="Tic Tac Toe Logo" class="w-12 h-12">
              </picture>
              <span class="text-xl font-bold"> Tic Tac Toe </span>
            </RouterLink>
          </div>

          <div class="flex items-center space-x-4">
            <button
              class="p-2.5 rounded-full flex items-center space-x-2 cursor-pointer transition-all duration-300 hover:shadow-md group"
              @click="themeStore.toggleTheme"
            >
              <div class="relative w-5 h-5">
                <svg
                  v-if="themeStore.theme === 'dark'"
                  class="w-5 h-5 text-yellow-300"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                    clip-rule="evenodd"
                  />
                </svg>
                <svg v-else class="w-5 h-5 text-blue-900" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              </div>
            </button>

            <div v-if="!authStore.isLoggedIn" class="flex items-center space-x-3">
              <button
                class="cursor-pointer px-4 py-2 text-sm font-medium hover:text-gray-400"
                @click="openAuthModal('login')"
              >
                Log in
              </button>
              <button
                class="cursor-pointer px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                @click="openAuthModal('signup')"
              >
                Sign up
              </button>
            </div>
            <div v-else class="flex items-center space-x-3">
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
            </div>
          </div>
        </div>
      </div>
    </nav>
    <main class="grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="max-w-6xl mx-auto">
        <slot />
      </div>
    </main>
    <footer class="border-t border-custom-transparent">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col items-center justify-center space-y-4 mt-4 mb-4 text-center">
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
