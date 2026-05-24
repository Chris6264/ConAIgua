import { User } from "lucide-react";
import "./LoginButton.css";

export const LoginButton = ({ children, href = "#login" }) => {
  return (
    <a href={href} className="login-button">
      <User size={20} />
      <span>{children}</span>
    </a>
  );
};