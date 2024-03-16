import React from "react";
import QueueAnim from "rc-queue-anim";
import "../components_css/intro.css";
import { useNavigate } from "react-router-dom";

export default function Page1() {
  let navigate = useNavigate();
  const regression = () => {
    navigate("/regression");
  };
  const classification = () => {
    navigate("/classification");
  };
  const object_detection = () => {
    navigate("/object_detection");
  };

  return (
    <div className="page-wrapper page1">
      <div className="row" id="card_row">
        <div className="col-4">
          <QueueAnim>
            <div className="card1" onClick={regression}>
              <div className="align">
                <span className="red"></span>
                <span className="yellow"></span>
                <span className="green"></span>
              </div>

              <h1 id="h1">Regression</h1>
            </div>
          </QueueAnim>
        </div>
        <div className="col-4">
          <div className="card2" onClick={classification}>
            <div className="align">
              <span className="red"></span>
              <span className="yellow"></span>
              <span className="green"></span>
            </div>
            <h1 className="classification">Classification</h1>
          </div>
        </div>
        <div className="col-4">
          <div className="card3" onClick={object_detection}>
            <div className="align">
              <span className="red"></span>
              <span className="yellow"></span>
              <span className="green"></span>
            </div>
            <h1>Object Detection</h1>
          </div>
        </div>
      </div>
    </div>
  );
}
