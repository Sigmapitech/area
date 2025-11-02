#!/bin/bash

# Output dir
OUTPUT_DIR=/app
APK_NAME=client.apk

# Ensure output folder exist
mkdir -p $OUTPUT_DIR
npx cap sync android
cd android
# Clean previous build
./gradlew clean

# Sync dependencies
./gradlew build --no-daemon --refresh-dependencies

# Build project for release
./gradlew assembleRelease

# Copy apk to output dir
cp /build/android/app/build/outputs/apk/release/app-release.apk $OUTPUT_DIR/$APK_NAME

# Ensure build success
if [ -f "$OUTPUT_DIR/$APK_NAME" ]; then
    echo "APK successfully generated : $OUTPUT_DIR/$APK_NAME"
else
    echo "APK generation failed."
    exit 1
fi
