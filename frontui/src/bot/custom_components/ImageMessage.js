import React from 'react';

const ImageMessage = ({payload}) => {
  return (
    <img
      src={payload}
      alt={payload}
      style={{ width: '100%' }}
    />
  );
};

export default ImageMessage;