# Nix builder
FROM nixos/nix:latest AS builder

# Copy our source and setup our working dir.
COPY . /tmp/build
WORKDIR /tmp/build

# Build our Nix environment (server backend)
RUN nix \
    --extra-experimental-features "nix-command flakes" \
    --option filter-syscalls false \
    build .#back

# Copy the Nix store closure into a directory.
RUN mkdir /tmp/nix-store-closure
RUN cp -R $(nix-store -qR result/) /tmp/nix-store-closure

# Final image is based on scratch.
FROM scratch

# Copy /nix/store and the built result
COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app
COPY --from=builder /tmp/build/back/config.toml /app/config.toml

# Expose server port and run
ENV PORT=8080
WORKDIR /app
EXPOSE 8080
# Pass "dev" to enable the CORS branch in app.main
CMD ["/app/bin/area", "run"]
