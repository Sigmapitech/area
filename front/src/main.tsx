import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.scss";
import App from "./App.tsx";

// biome-ignore lint: root node existence is granted
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
