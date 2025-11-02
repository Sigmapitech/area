FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt install -y nodejs \
    && corepack enable

WORKDIR /app

COPY . .
ENV CI=true

RUN pnpm install --frozen-lockfile
RUN pnpm build:web

EXPOSE 8081
CMD ["serve", "-s", "dist", "-l", "8081"]
