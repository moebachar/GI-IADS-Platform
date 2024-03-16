import React from "react";
import PropTypes from "prop-types";
import QueueAnim from "rc-queue-anim";
import { Button } from "antd";
import { Element } from "rc-scroll-anim";
import BannerImage from "./BannerImage";
import { assets } from "./data";

class Banner extends React.PureComponent {
  static propTypes = {
    className: PropTypes.string,
    isMobile: PropTypes.bool,
    navToShadow: PropTypes.func,
  };
  static defaultProps = {
    className: "banner",
  };
  render() {
    const { className, isMobile, navToShadow } = this.props;
    return (
      <Element
        component="section"
        className={`${className}-wrapper page`}
        onChange={navToShadow}
      >
        <div className={className}>
          <div className={`${className}-img-wrapper`}>
            {isMobile ? (
              <img
                width="100%"
                src={`${assets}/image/home/intro-landscape-3a409.svg`}
                alt=""
              />
            ) : (
              <BannerImage />
            )}
          </div>
          <QueueAnim
            type={isMobile ? "bottom" : "right"}
            className={`${className}-text-wrapper`}
            delay={300}
          >
            <h1 key="h1">GI-IADS Platform</h1>
            <p className="main-info" key="p">
              GI-IADS is your no-code gateway to the world of machine learning,
              simplifying complex algorithms into an intuitive platform for
              effortless data-driven insights. With GI-IADS, empower your team
              to harness the full potential of machine learning without the need
              for coding expertise.
            </p>
            <a
              // target="_blank"
              key="a"
            >
              {/* <Button type="primary">Learn more</Button> */}
              <button className="btn btn-primary" id="learnmore">
                Learn more
              </button>
            </a>
          </QueueAnim>
        </div>
      </Element>
    );
  }
}

export default Banner;
