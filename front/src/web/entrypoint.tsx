import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";

import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import WorkflowList from "@/routes/workflow_create";

function WebApp() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<LoginRequired />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/graph" element={<WorkflowList />} />
            <Route path="/graph/:id" element={<GraphPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default WebApp;
