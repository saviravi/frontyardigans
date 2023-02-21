import React from 'react';

const ImageMessage = props => {
  return (
    <img
      src={props.payload}
      style={{ width: '100%' }}
    />
  );
};

export default ImageMessage;