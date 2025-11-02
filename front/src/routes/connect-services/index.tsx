import { App } from "@capacitor/app";
import { Browser } from "@capacitor/browser";
import { useEffect, useState, useCallback } from "react";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import "./style.scss";

function getPopupDimension() {
  const width = 500;
  const height = 700;
  const left = window.screenX + (window.innerWidth - width) / 2;
  const top = window.screenY + (window.innerHeight - height) / 2;
  return [width, height, left, top];
}

export default function ConnectServicesPage() {
  const { token } = useAuth();
  const [services, setServices] = useState<Record<string, string>>({});
  const [connected, setConnected] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = useCallback(
    async (isInitial = false) => {
      try {
        if (isInitial) setLoading(true);
        const [servicesRes, meRes] = await Promise.all([
          fetch(`${API_BASE_URL}/services`),
          fetch(`${API_BASE_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        if (!servicesRes.ok || !meRes.ok) throw new Error("Fetch failed");

        const servicesData = await servicesRes.json();
        const meData = await meRes.json();

        setServices(servicesData);
        setConnected(meData.services || {});
      } catch (err) {
        console.error("Failed to fetch services:", err);
      } finally {
        if (isInitial) setLoading(false);
        setRefreshing(false);
      }
    },
    [token]
  );

  useEffect(() => {
    fetchData(true);
  }, [fetchData]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData(false); // don’t trigger global loading
  };

  const handleConnect = (service: string) => {
    const connectUrl = `${API_BASE_URL}/${service}/connect?token=${token}&platform=${__APP_PLATFORM__}`;

    if (__APP_PLATFORM__ === "mobile") {
      App.addListener("appUrlOpen", async (data) => {
        const url = new URL(data.url);
        const code = url.searchParams.get("code");
        if (code) {
          await Browser.close();
          setConnected((prev) => ({ ...prev, [service]: true }));
        }
      });

      Browser.open({ url: connectUrl });
    } else {
      const [width, height, left, top] = getPopupDimension();
      const popup = window.open(
        connectUrl,
        "_blank",
        `width=${width},height=${height},left=${left},top=${top}`
      );

      const listener = (event: MessageEvent) => {
        if (event.data?.type === `${service.toUpperCase()}_CONNECTED`) {
          popup?.close();
          setConnected((prev) => ({ ...prev, [service]: true }));
          window.removeEventListener("message", listener);
        }
      };
      window.addEventListener("message", listener);
    }
  };

  if (loading) return <div>Loading services...</div>;

  return (
    <div className={`service-page ${refreshing ? "dimmed" : ""}`}>
      <h1>Services</h1>
      <div>
        <button
          className="service-page-refresh"
          onClick={handleRefresh}
          disabled={refreshing}
        >
          Refresh
        </button>
      </div>

      <div className="service-list">
        {Object.entries(services).map(([name, svg]) => {
          const isConnected = connected[name] ?? false;
          return (
            <div className="service-card" key={name}>
              <div
                className="service-card-icon"
                dangerouslySetInnerHTML={{ __html: svg }}
              />
              <div className="service-card-description">
                <p className="service-card-name">{name}</p>
              </div>
              {!isConnected && (
                <button type="button" onClick={() => handleConnect(name)}>
                  Connect
                </button>
              )}
              {isConnected && <span className="connected-tag">Connected</span>}
            </div>
          );
        })}
      </div>
    </div>
  );
}
