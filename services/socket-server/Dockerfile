# Stage 1: Сборка
FROM golang:1.22-alpine AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей (для кэширования слоев Docker)
COPY go.mod go.sum ./
RUN go mod download

# Копируем все исходники
COPY . .

# Собираем бинарник. 
# CGO_ENABLED=0 нужен для статической линкoвки (чтобы работало в alpine/scratch)
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server ./cmd/server/main.go

# Stage 2: Финальный образ
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Копируем только скомпилированный файл из предыдущего этапа
COPY --from=builder /app/server .
# Если у тебя есть конфиги или .env, которые нужны при запуске:
# COPY --from=builder /app/config ./config 

# Открываем порт (тот, что указан в твоем сервисе)
EXPOSE 8080

# Запускаем
CMD ["./server"]