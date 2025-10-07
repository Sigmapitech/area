import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import { CheckAPIConnection } from "./api-guard";
import Burger, { useOnClickOutside } from "@/mobile/composant/burger-menu";
import { useRef, useState } from "react";

function MobileApp() {
  const [open, setOpen] = useState(false);
  const node = useRef<HTMLDivElement>(null);

  useOnClickOutside(node, () => setOpen(false));

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CheckAPIConnection />} />

          <Route path="/login" element={<LoginPage />} />
          <Route element={<LoginRequired />}>
            <Route path="/home" element={<HomePage />} />
            <Route path="/graph" element={<GraphPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default MobileApp;
