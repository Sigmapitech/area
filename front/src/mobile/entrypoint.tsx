import { BrowserRouter, Route, Routes } from "react-router";
import "@/index.scss";

function MobileApp() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<p>Mobile</p>} />
      </Routes>
    </BrowserRouter>
  );
}

export default MobileApp;
