FROM oven/bun:1 AS build-stage

WORKDIR /app

COPY package.json bun.lock* ./

RUN bun install --frozen-lockfile

COPY . .

RUN bun run build-only

CMD cp -rt /output /app/dist/*
