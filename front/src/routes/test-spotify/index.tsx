import { StrictMode, useState } from "react";

import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import { App } from "@capacitor/app";
import { Browser } from "@capacitor/browser";

function getPopupDimension() {
  const width = 500;
  const height = 700;
  const left = window.screenX + (window.innerWidth - width) / 2;
  const top = window.screenY + (window.innerHeight - height) / 2;

  return [width, height, left, top];
}

export default function TestSpotifyPage() {
  const { token } = useAuth();

  const [connected, setConnected] = useState<boolean>(false);
  const [spotifyData, setData] = useState<object>({});

  const connectDiscord = () => {
    if (__APP_PLATFORM__ == "mobile") {
      window.addEventListener("message", (event) => {
        console.log(event.data?.type);
        if (event.data?.type === "SPOTIFY_CONNECTED") {
          setConnected(true);
          console.log("linked!", event.data.payload);
          fetchData();
        }
      });

      App.addListener("appUrlOpen", async (data) => {
        console.log("Deep link opened:", data.url);
        const url = new URL(data.url);
        const code = url.searchParams.get("code");

        if (code) {
          await Browser.close();
          console.log("Got Spotify code:", code ?? "no-code");
          setConnected(true);
          fetchData();
        }
      });

      Browser.open({
        url: `${API_BASE_URL}/spotify/connect?token=${token}&platform=${__APP_PLATFORM__}`,
      });
      // just assume it works
    } else {
      const [width, height, left, top] = getPopupDimension();
      const popup = window.open(
        `${API_BASE_URL}/spotify/connect?token=${token}&platform=${__APP_PLATFORM__}`,
        "_system",
        `width=${width},height=${height},left=${left},top=${top}`
      );

      window.addEventListener("message", (event) => {
        console.log(event.data?.type);
        if (event.data?.type === "SPOTIFY_CONNECTED") {
          setConnected(true);
          console.log("linked!", event.data.payload);
          popup?.close();
          fetchData();
        }
      });
    }
  };

  const fetchData = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/spotify/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to fetch");
      }

      const data = await res.json();
      console.log(data);
      setData(data);
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <StrictMode>
      <div className="test-spotify" style={{ padding: "1em" }}>
        {(!connected && (
          <button type="button" onClick={connectDiscord}>
            Connect with Spotify
          </button>
        )) || (
          <>
            <p>Connected!</p>
            <pre>{JSON.stringify(spotifyData, null, 2)}</pre>
          </>
        )}
      </div>
    </StrictMode>
  );
}
