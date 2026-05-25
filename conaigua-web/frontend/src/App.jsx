import React from "react";
import { Navbar } from "./components/navbar/Navbar";
import { CircleIcon } from "./components/icons/circle-icon/CircleIcon";
import { CloudRain, Droplet } from "lucide-react";
import { WelcomeText } from "./components/texts/welcome-text/WelcomeText";
import { AuthCard } from "./components/cards/authcard/AuthCard";
import conaiguaVideo from "./assets/conaigua-video-preview.mp4"
import { VideoPreview } from "./components/videos/video-preview/VideoPreview";
import "./App.css";

export function App() {
  return (
    <div>frontend/src/assets/conaigua-video-preview.mp4
      <Navbar />
      <main className="main-content">
        <CircleIcon
          icon={CloudRain}
          variant="rain"
          className="hero-icon-rain"
          size={70}
        />
        <WelcomeText className="hero-welcome-text" />
        <AuthCard className="hero-auth-card" />
        <VideoPreview className="hero-video-preview" video={conaiguaVideo} />
      </main>
    </div>
  );
}
