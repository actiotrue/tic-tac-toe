import { ref } from "vue";

export function useTurnTimer(seconds: number) {
  const secondsLeft = ref<number>(seconds);
  const initialSeconds = ref(seconds);

  let timerInterval: number | null = null;

  const start = (seconds: number) => {
    if (timerInterval)
      clearInterval(timerInterval);
    secondsLeft.value = seconds;

    timerInterval = window.setInterval(() => {
      if (secondsLeft.value > 0) {
        secondsLeft.value--;
      }
      else {
        clearInterval(timerInterval!);
      }
    }, 1000);
  };

  const stop = () => {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
  };

  const reset = (newSeconds?: number) => {
    secondsLeft.value = newSeconds ?? initialSeconds.value;
  };
  return {
    secondsLeft,
    start,
    stop,
    reset,
  };
}
