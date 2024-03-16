import React from "react";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";

export default function Header(props) {
  let navigate = useNavigate();
  const homepage = () => {
    navigate("/");
  };

  return (
    <header {...props}>
      <div
        className="logo-wrapper"
        onClick={homepage}
        // target="_blank"
      >
        <i className="logo" />
        <span>GI-IADS Platform</span>
      </div>
      <div className="button">
        {/* <Button>Contact us</Button> */}
        <button className="btn btn-light" id="contactus">
          Contact us
        </button>
      </div>
    </header>
  );
}
