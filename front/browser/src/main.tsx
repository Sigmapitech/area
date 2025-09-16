import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import NotFoundPage from "./routes/404";
import HomePage from "./routes/home";

const root = document.getElementById("root");
if (!root) throw new Error("Root element not found");

ReactDOM.createRoot(root).render(
  <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  </>
);
