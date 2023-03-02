import React from 'react';
import '../../App.css'

const ImageMessage = ({payload}) => {
  return (
    <img
      src={payload}
      alt={payload}
      className="image-message"
    />
  );
};

export default ImageMessage;