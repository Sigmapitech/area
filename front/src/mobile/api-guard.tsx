import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { API_BASE_URL } from "@/api_url";

export function CheckAPIConnection() {
  const [status, setStatus] = useState<"loading" | "ok" | "error" | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    setStatus("loading");
    try {
      const res = await fetch(`${API_BASE_URL}/api/hello`);
      if (res.ok) {
        setStatus("ok");
        navigate("/home");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  const skip = () => {
    navigate("/home");
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div style={{ display: "grid", placeItems: "center" }}>
      {loading && <p>Checking API...</p>}
      {!loading && status === "error" && (
        <p>Cannot reach API at {API_BASE_URL}.</p>
      )}

      <div
        style={{
          textAlign: "left",
        }}
      >
        <pre>adb devices</pre>
        <pre>adb -s [device] reverse tcp:8080 tcp:8080</pre>
      </div>
      <br />
      <div style={{ display: "flex", gap: "1em" }}>
        <button type="button" onClick={fetchData}>
          Retry
        </button>
        <button type="button" onClick={skip}>
          Skip anyway
        </button>
      </div>
    </div>
  );
}
