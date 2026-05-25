import "./WelcomeText.css";

export function WelcomeText({ className = "" }) {
  return (
    <section className={`welcome-text ${className}`}>
      <h1>
        Consulta datos <br />
        hidrometeorológicos <br />
        con el poder de la <span>IA</span>
      </h1>

      <p>
        Analiza, visualiza y toma mejores decisiones con datos de estaciones
        climatológicas e inteligencia artificial.
      </p>
    </section>
  );
}

export default WelcomeText;