# Nix builder
FROM nixos/nix:latest AS builder

# Copy our source and setup our working dir.
COPY .. /tmp/build
WORKDIR /tmp/build

# Build our Nix environment (front-web helper)
RUN nix \
    --extra-experimental-features "nix-command flakes" \
    --option filter-syscalls false \
    build .#front

# Copy the Nix store closure into a directory.
RUN mkdir /tmp/nix-store-closure
RUN cp -R $(nix-store -qR result/) /tmp/nix-store-closure

# Final image is based on scratch.
FROM scratch

# Copy /nix/store and the built result
COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app

# Expose client_web port and run
EXPOSE 8081
CMD ["/app/bin/web"]
