import React, { useState } from "react";
import "./Navbar.css";
import logo from "../../assets/conaigua-logo.png";
import { LoginButton } from "../buttons/login-button/LoginButton";

const Navbar = () => {
  const [activeLink, setActiveLink] = useState("inicio");

  return (
    <header className="header">
      <div className="header-container">
        <a href="/" className="logo">
          <img src={logo} alt="Logo ConAIgua" />
        </a>

        <div className="header-right">
          <nav className="navbar">
            <a
              href="/"
              className={`navbar-link ${activeLink === "inicio" ? "active" : ""}`}
              onClick={() => setActiveLink("inicio")}
            >
              Inicio
            </a>

            <a
              href="#acerca"
              className={`navbar-link ${activeLink === "acerca" ? "active" : ""}`}
              onClick={() => setActiveLink("acerca")}
            >
              Acerca de
            </a>

            <a
              href="#funciones"
              className={`navbar-link ${activeLink === "funciones" ? "active" : ""}`}
              onClick={() => setActiveLink("funciones")}
            >
              ¿Qué puedes hacer?
            </a>

            <a
              href="#preguntas"
              className={`navbar-link ${activeLink === "preguntas" ? "active" : ""}`}
              onClick={() => setActiveLink("preguntas")}
            >
              Preguntas Frecuentes
            </a>
          </nav>

          <LoginButton href="/login">Iniciar sesión</LoginButton>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
