import "./VideoPreview.css";

export function VideoPreview({ className = "", video }) {
  return (
    <section className={`video-preview ${className}`}>
      <video className="video-preview-player" controls>
        <source src={video} type="video/mp4" />
      </video>
    </section>
  );
}