import { ref } from "vue";

export function useWebSocket<T = any>(url: string) {
  const ws = ref<WebSocket | null>(null);

  const connect = (options?: {
    onOpen?: () => void;
    onMessage?: (data: T) => void;
    onError?: (err: string) => void;
    onClose?: (reason: string) => void;
  }) => {
    const socket = new WebSocket(url);

    if (options?.onOpen)
      socket.onopen = options.onOpen;
    if (options?.onError)
      socket.onerror = () => options.onError!("Error while connecting to the server");
    if (options?.onClose)
      socket.onclose = (event: CloseEvent) => options.onClose!(event.reason);

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

  return { connect, send, ws };
}
