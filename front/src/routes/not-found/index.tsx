import { Link } from "react-router";
import "./style.scss";

export default function NotFoundPage() {
  return (
    <div className="notfound-page">
      <div className="notfound-content">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>Sorry, the page you are looking for does not exist.</p>
        <Link to="/" className="btn">
          Go Home
        </Link>
      </div>
    </div>
  );
}
