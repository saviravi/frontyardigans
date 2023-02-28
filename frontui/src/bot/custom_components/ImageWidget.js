import React from 'react';

/* Not actually used at the moment but a good example for a widget */
const ImageWidget = (props) => {
  return (
    <div>
      <img className="image-message" src={props.payload} alt={props.payload} />
    </div>
  );
};

export default ImageWidget;