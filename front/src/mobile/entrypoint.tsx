import { useRef, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import Burger, { useOnClickOutside } from "@/mobile/composant/burger-menu";
import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import { CheckAPIConnection } from "./api-guard";

function MobileApp() {
  const [open, setOpen] = useState(false);
  const node = useRef<HTMLDivElement>(null);

  useOnClickOutside(node, () => setOpen(false));

  return (
    <AuthProvider>
      <Burger open={open} setOpen={setOpen}>
        <p>test thingie</p>
        <p>test 2</p>
      </Burger>
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
