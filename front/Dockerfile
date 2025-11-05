FROM node:22-bookworm-slim AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN corepack enable && corepack prepare pnpm@latest --activate

RUN npm install -g serve

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

ENV CI=true
RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm build:web

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose to 80 and remap it in compose since nginx defaults to 80 without parameters possible
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
