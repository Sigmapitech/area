import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import MainLayout from "@/layouts/main";
import ConnectServicesPage from "@/routes/connect-services";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import ProfilePage from "@/routes/profile";
import RegisterPage from "@/routes/register";
import WorkflowEditor from "@/routes/workflow";
import WorkflowList from "@/routes/workflow-create";
import { CheckAPIConnection } from "./api-guard";

function MobileApp() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CheckAPIConnection />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route element={<MainLayout />}>
            <Route element={<LoginRequired />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/home" element={<HomePage />} />
              <Route path="/workflow" element={<WorkflowList />} />
              <Route
                path="/workflow/:workflowId"
                element={<WorkflowEditor />}
              />
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
