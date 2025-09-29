import { BrowserRouter, Route, Routes } from "react-router";

import { AuthProvider, LoginRequired } from "@/auth";

import "./index.scss";

import GraphPage from "@/routes/graph";
import HomePage from "@/routes/home";
import LoginPage from "@/routes/login";

function MobileApp() {
  return (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<LoginRequired />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/graph" element={<GraphPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </AuthProvider>
  );
}

export default MobileApp;
