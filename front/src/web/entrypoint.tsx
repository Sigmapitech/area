import { BrowserRouter, Routes, Route } from "react-router";
import "@/index.scss";

function WebApp() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<p>Web</p>} />
      </Routes>
    </BrowserRouter>
  );
}

export default WebApp;
