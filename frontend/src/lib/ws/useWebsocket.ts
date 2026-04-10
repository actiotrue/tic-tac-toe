import type { Ref } from "vue";

import { ref } from "vue";

export function useWebSocket<T = any>(urlRef: Ref<string>) {
  const ws = ref<WebSocket | null>(null);

  const connect = (options?: {
    onOpen?: () => void;
    onMessage?: (data: T) => void;
    onError?: (err: string) => void;
    onClose?: (reason: string) => void;
  }) => {
    if (!urlRef.value) {
      console.error("WebSocket URL is empty");
      return;
    }
    const socket = new WebSocket(urlRef.value);

    if (options?.onOpen)
      socket.onopen = options.onOpen;
    if (options?.onError)
      socket.onerror = () => options.onError!("Error while connecting to the server");
    if (options?.onClose) {
      socket.onclose = (event: CloseEvent) => {
        const reason = event.reason?.trim();
        options.onClose!(reason || `Connection closed (code ${event.code})`);
      };
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        options?.onMessage?.(data);
      }
      catch {
        console.error("Invalid JSON", event.data);
      }
    };

    ws.value = socket;
  };

  const send = (data: any) => {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data));
    }
  };

  const close = () => {
    if (ws.value) {
      ws.value.close();
    }
  };

  return { connect, send, close, ws };
}
