#!/bin/bash

# TechDoc Manager - Build Script
# This script builds the debug APK for TechDoc Manager

echo "=========================================="
echo "  TechDoc Manager - APK Build Script"
echo "=========================================="
echo ""

# Check for Java
if ! command -v java &> /dev/null; then
    echo "❌ Error: Java is not installed"
    echo "Please install JDK 17 or higher"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "❌ Error: Java 17 or higher is required (found: $JAVA_VERSION)"
    exit 1
fi
echo "✅ Java version: OK"

# Check for Android SDK
if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "⚠️  Warning: ANDROID_HOME or ANDROID_SDK_ROOT not set"
    echo "Trying to auto-detect Android SDK..."

    # Common Android SDK locations
    POSSIBLE_PATHS=(
        "$HOME/Android/Sdk"
        "$HOME/Library/Android/sdk"
        "/usr/local/android-sdk"
        "/opt/android-sdk"
    )

    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -d "$path" ]; then
            export ANDROID_HOME="$path"
            export ANDROID_SDK_ROOT="$path"
            echo "✅ Found Android SDK at: $path"
            break
        fi
    done

    if [ -z "$ANDROID_HOME" ]; then
        echo "❌ Error: Android SDK not found"
        echo "Please install Android SDK and set ANDROID_HOME environment variable"
        exit 1
    fi
else
    echo "✅ Android SDK: ${ANDROID_HOME:-$ANDROID_SDK_ROOT}"
fi

# Build the APK
echo ""
echo "🔨 Building debug APK..."
echo ""

./gradlew assembleDebug --no-daemon

if [ $? -eq 0 ]; then
    APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
    if [ -f "$APK_PATH" ]; then
        echo ""
        echo "=========================================="
        echo "✅ Build successful!"
        echo "=========================================="
        echo ""
        echo "APK location: $APK_PATH"
        echo "APK size: $(du -h "$APK_PATH" | cut -f1)"
        echo ""
        echo "To install on connected device:"
        echo "  adb install $APK_PATH"
    else
        echo "❌ APK file not found at expected location"
        exit 1
    fi
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the error messages above for details"
    exit 1
fi
