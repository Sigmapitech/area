import { Link } from "react-router";

import "./style.scss";

export default function NotFoundPage() {
  return (
    <div className="center-div">
      <div className="container gradient-card">
        <h1>404 - Page Not Found</h1>
        <p>Sorry, the page you are looking for does not exist.</p>
        <Link to="/">Go back to Home</Link>
      </div>
    </div>
  );
}
