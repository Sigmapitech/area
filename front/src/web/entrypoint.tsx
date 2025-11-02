import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import MainLayout from "@/layouts/main";
import ConnectServicesPage from "@/routes/connect-services";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import ProfilePage from "@/routes/profile";
import RegisterPage from "@/routes/register";
import TestSpotifyPage from "@/routes/test-spotify";
import GraphPage from "@/routes/workflow";
import WorkflowList from "@/routes/workflow-create";

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
              <Route path="/workflow" element={<WorkflowList />} />
              <Route path="/workflow/:workflowId" element={<GraphPage />} />
              <Route path="/test-spotify" element={<TestSpotifyPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/services" element={<ConnectServicesPage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default WebApp;
