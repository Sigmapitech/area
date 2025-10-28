FROM nixos/nix:latest AS builder

COPY ../.. /tmp/build
WORKDIR /tmp/build

RUN nix \
    --extra-experimental-features "nix-command flakes" \
    --option filter-syscalls false \
    develop --command sh -c "echo 'Nix shell ready'"

RUN nix-env -iA nixpkgs.glibc nixpkgs.zlib nixpkgs.libgcc nixpkgs.aapt nixpkgs.android-tools

# ---- Gradle build (using system aapt2) ----
# Disable Gradle’s internal aapt2 binary
# Provide system aapt under the name `aapt2`
ENV ANDROID_AAPT2_FROM_BUILD_SERVICE=false
RUN ln -s "$(which aapt)" /usr/local/bin/aapt2

RUN nix develop --extra-experimental-features "nix-command flakes" --option filter-syscalls false --command \
    sh -c "cd front/android && ./gradlew assembleDebug --no-daemon --stacktrace"

RUN mkdir /tmp/nix-store-closure
RUN cp -R $(nix-store -qR result/) /tmp/nix-store-closure

FROM scratch

COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app

ENV PORT=8080
WORKDIR /app
EXPOSE 8080
CMD ["/app/bin/area", "dev"]
