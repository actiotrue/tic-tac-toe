FROM oven/bun:1 AS build-stage

WORKDIR /app

COPY package.json bun.lock* ./

RUN bun install --frozen-lockfile

COPY . .

RUN bun run build-only


FROM scratch AS export-stage

COPY --from=build-stage /app/dist /
