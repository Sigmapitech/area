import { BrowserRouter, Route, Routes } from "react-router";
import { AuthProvider, LoginRequired } from "@/auth";
import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";
import { CheckAPIConnection } from "./api-guard";

function MobileApp() {
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
