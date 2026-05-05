<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

interface Question {
  id: number;
  question: string;
  options: string[];
  correct: number;
  fact: string;
}

const props = defineProps<{
  questions: Question[];
}>();

const currentIndex = ref(Math.floor(Math.random() * props.questions.length));
const selectedAnswer = ref<number | null>(null);
const isCorrect = ref<boolean | null>(null);

const shuffledOptionIndices = ref<number[]>([]);

const currentQuestion = computed(() => props.questions[currentIndex.value]);

function shuffleOptions() {
  const indices = currentQuestion.value.options.map((_, i) => i);
  shuffledOptionIndices.value = indices.sort(() => Math.random() - 0.5);
}

onMounted(() => {
  shuffleOptions();
});

function handleAnswer(originalIndex: number) {
  if (selectedAnswer.value !== null)
    return;

  selectedAnswer.value = originalIndex;
  isCorrect.value = originalIndex === currentQuestion.value.correct;

  setTimeout(() => {
    nextQuestion();
  }, 3000);
}

function nextQuestion() {
  selectedAnswer.value = null;
  isCorrect.value = null;
  currentIndex.value = (currentIndex.value + 1) % props.questions.length;
  shuffleOptions();
}
</script>

<template>
  <div class="quiz-container">
    <div class="quiz-card">
      <p class="question-text">
        {{ currentQuestion.question }}
      </p>

      <div class="options">
        <button
          v-for="(option, index) in currentQuestion.options"
          :key="index"
          class="bg-quiz-button" :class="{
            correct: selectedAnswer !== null && index === currentQuestion.correct,
            wrong: selectedAnswer === index && index !== currentQuestion.correct,
            disabled: selectedAnswer !== null,
          }"
          @click="handleAnswer(index)"
        >
          {{ option }}
        </button>
      </div>

      <Transition name="fade">
        <div v-if="selectedAnswer !== null" class="feedback">
          <p v-if="isCorrect" class="text-success">
            Correct! 🎉
          </p>
          <p v-else class="text-error">
            ❌ Right answer is {{ currentQuestion.options[currentQuestion.correct] }}
          </p>
          <small class="text-sm">{{ currentQuestion.fact }}</small>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  padding: 20px;
  border-radius: 12px;
  max-width: 400px;
  margin: 20px auto;
}

.options {
  display: grid;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 12px;
  border: 1px solid #444;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

button:hover:not(.disabled) {
  background: #96999b;
}

button.correct {
  background: #2ecc71 !important;
  border-color: #27ae60;
}

button.wrong {
  background: #e74c3c !important;
  border-color: #c0392b;
}

button.disabled {
  cursor: default;
}

.feedback {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #444;
}

.text-success {
  color: #2ecc71;
}
.text-error {
  color: #e74c3c;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
