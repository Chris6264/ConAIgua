import "./AuthCard.css";
import { Mail, LockKeyhole } from "lucide-react";
import googleIcon from "../../../assets/google-icon.png";
import { ButtonWithImage } from "../../buttons/button-with-image/ButtonWithImage";
import { ButtonWithIcon } from "../../buttons/button-with-icon/ButtonWithIcon";

export function AuthCard({ className = "" }) {
  return (
    <section className={`auth-card ${className}`}>
      <ButtonWithImage className="auth-card-google-button" image={googleIcon}>
        Continuar con Google
      </ButtonWithImage>

      <div className="auth-card-divider">
        <span></span>
        <p>o</p>
        <span></span>
      </div>

      <ButtonWithIcon href="#login" className="email-login-button" icon={Mail}>
        Ingresa tu correo
      </ButtonWithIcon>

      <a href="#terms" className="auth-card-terms">
        <LockKeyhole size={18} />
        <span>Términos y condiciones</span>
      </a>
    </section>
  );
}