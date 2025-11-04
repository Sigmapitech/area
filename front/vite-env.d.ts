// vite-env.d.ts

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly PROD: boolean;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare const __APP_PLATFORM__: "mobile" | "web";
