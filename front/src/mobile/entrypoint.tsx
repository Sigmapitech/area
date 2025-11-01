import { useRef, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import TestSpotifyPage from "@/routes/test-spotify";
import GraphPage from "@/routes/workflow";
import WorkflowList from "@/routes/workflow-create";
import { CheckAPIConnection } from "./api-guard";
import MainLayout from "@/layouts/main";

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
            <Route element={<MainLayout />}>
              <Route path="/home" element={<HomePage />} />
              <Route path="/graph" element={<WorkflowList />} />
              <Route path="/test-spotify" element={<TestSpotifyPage />} />
            </Route>
            <Route path="/graph/:id" element={<GraphPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default MobileApp;
