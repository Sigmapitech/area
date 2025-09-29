import { BrowserRouter, Route, Routes } from "react-router";
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
