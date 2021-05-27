import React, { useState } from "react";
import { FaStar } from "react-icons/fa";

const StarRating = () => {
  return (
    <>
      {[...Array(5)].map((i) => (
        <FaStar color={"#ff4400"} className="star" />
      ))}
    </>
  );
};

export default StarRating;
