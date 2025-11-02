import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import MainLayout from "@/layouts/main";
import ConnectServicesPage from "@/routes/connect-services";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import TestSpotifyPage from "@/routes/test-spotify";
import GraphPage from "@/routes/workflow";
import WorkflowList from "@/routes/workflow-create";
import { CheckAPIConnection } from "./api-guard";

function MobileApp() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CheckAPIConnection />} />
          <Route path="/login" element={<LoginPage />} />
          <Route element={<MainLayout />}>
            <Route element={<LoginRequired />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/home" element={<HomePage />} />
              <Route path="/graph" element={<WorkflowList />} />
              <Route path="/test-spotify" element={<TestSpotifyPage />} />
              <Route path="/graph/:id" element={<GraphPage />} />
              <Route path="/services" element={<ConnectServicesPage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default MobileApp;
