import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import MainLayout from "@/layouts/main";
import ConnectServicesPage from "@/routes/connect-services";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import GraphPage from "@/routes/workflow";
import WorkflowList from "@/routes/workflow-create";
import { CheckAPIConnection } from "./api-guard";
import ProfilePage from "@/routes/profile";

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
              <Route path="/graph/:id" element={<GraphPage />} />
              <Route path="/services" element={<ConnectServicesPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default MobileApp;
