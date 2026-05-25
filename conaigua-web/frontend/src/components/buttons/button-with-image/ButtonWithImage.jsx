import "./ButtonWithImage.css";

export function ButtonWithImage ({children, image}){
    return (
        <button className="button-with-image">
        {image && <img src={image} alt='' />}
        <span>{children}</span>
        </button>
    )
}