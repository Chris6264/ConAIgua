import { User } from "lucide-react";
import "./ButtonWithIcon.css";

export function ButtonWithIcon({
  children,
  href = "",
  icon: Icon = User,
  className = "",
}) {
  return (
    <a href={href} className={`button-with-icon ${className}`}>
      <Icon size={20} />
      <span>{children}</span>
    </a>
  );
}