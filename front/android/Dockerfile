FROM node:20-bookworm-slim

# --- System Dependencies ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash curl unzip git ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Install OpenJDK 21 (Temurin) ---
RUN curl -L https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.9+10/OpenJDK21U-jdk_x64_linux_hotspot_21.0.9_10.tar.gz \
        -o /tmp/jdk21.tar.gz && \
    mkdir -p /usr/lib/jvm && \
    tar -xzf /tmp/jdk21.tar.gz -C /usr/lib/jvm && \
    rm /tmp/jdk21.tar.gz && \
    ln -s /usr/lib/jvm/jdk-21*/bin/java /usr/bin/java && \
    ln -s /usr/lib/jvm/jdk-21*/bin/javac /usr/bin/javac

ENV JAVA_HOME=/usr/lib/jvm/jdk-21.0.9+10/
ENV PATH="$JAVA_HOME/bin:$PATH"


# --- Install Android SDK ---
ENV ANDROID_SDK_ROOT="/sdk" \
    ANDROID_HOME="/sdk" \
    PATH="$PATH:/sdk/cmdline-tools/bin:/sdk/platform-tools"

RUN mkdir /sdk && \
    curl -s https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -o /cmdline-tools.zip && \
    unzip /cmdline-tools.zip -d /sdk/ && \
    rm /cmdline-tools.zip && \
    mkdir -p /sdk/cmdline-tools/latest && \
    mv /sdk/cmdline-tools/* /sdk/cmdline-tools/latest/ || true && \
    yes | /sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/sdk --install \
      "platform-tools" "platforms;android-35" "build-tools;35.0.0" "cmdline-tools;latest"

# --- Install Gradle ---
RUN curl -sL https://services.gradle.org/distributions/gradle-8.10-bin.zip -o gradle.zip && \
    mkdir /opt/gradle && \
    unzip gradle.zip -d /opt/gradle && \
    rm gradle.zip
ENV PATH="/opt/gradle/gradle-8.10/bin:$PATH"

# --- Install pnpm ---
RUN npm install -g pnpm

# --- Web Build ---
WORKDIR /build
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build:web
RUN npx cap sync android

# --- Prepare Android Build ---
RUN chmod +x /build/entrypoint.sh

CMD ["bash", "entrypoint.sh"]
