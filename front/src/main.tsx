import "./index.scss";

import MobileApp from "./mobile/entrypoint";
import WebApp from "./web/entrypoint";

import { createRoot } from "react-dom/client";
import { StrictMode } from "react";

// biome-ignore lint: root node is granted
const root = createRoot(document.getElementById("root")!);

root.render(
  __APP_PLATFORM__ === "web" ? (
    <StrictMode>
      <WebApp />
    </StrictMode>
  ) : (
    <StrictMode>
      <MobileApp />
    </StrictMode>
  )
);
