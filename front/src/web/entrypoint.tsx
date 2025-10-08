import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import MainLayout from "@/layouts/main";

import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import TestSpotifyPage from "@/routes/test-spotify";
import RegisterPage from "@/routes/register";
import WorkflowList from "@/routes/workflow-create";
import ProfilePage from "@/routes/profile";

function WebApp() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route element={<LoginRequired />}>
            <Route element={<MainLayout />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/graph" element={<WorkflowList />} />
              <Route path="/graph/:id" element={<GraphPage />} />
              <Route path="/test-spotify" element={<TestSpotifyPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default WebApp;
