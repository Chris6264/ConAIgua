import React from 'react'

export const ButtonWithImage = ({children, image}) => {
    return (
        <button>
        {image && <img src={image} alt='' />}
        <span>{children}</span>
        </button>
    )
}