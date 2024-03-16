import React from "react";
import { Row, Col } from "antd";

function Footer() {
  return (
    <footer id="footer" className="dark">
      <div className="footer-wrap">
        <Row justify="center" align="top">
          <Col lg={4} sm={24} xs={24}>
            <div className="footer-center">
              <h2>Regression</h2>
              <div>
                <a target="_blank " href="#">
                  Lorem
                </a>
              </div>
              <div>
                <a target="_blank " href="#">
                  API
                </a>
              </div>
              <div>
                <a href="#">Ipsum</a>
              </div>
            </div>
          </Col>
          <Col lg={4} sm={24} xs={24}>
            <div className="footer-center">
              <h2>Classification</h2>
              <div>
                <a href="#">Lorem</a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  API
                </a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  Ipsum
                </a>
              </div>
            </div>
          </Col>
          <Col lg={4} sm={24} xs={24}>
            <div className="footer-center">
              <h2>Computer Vision</h2>
              <div>
                <a href="#">Lorem</a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  API
                </a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  Ipsum
                </a>
              </div>
            </div>
          </Col>
          {/* <Col lg={4} sm={24} xs={24}>
            <div className="footer-center">
              <h2>墨者学院</h2>
              <div>
                <a href="#">博客</a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  设计原则
                </a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  图表用法
                </a>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="#">
                  资源
                </a>
              </div>
            </div>
          </Col> */}
          {/* <Col lg={8} sm={24} xs={24}>
            <div className="footer-center">
              <h2>更多产品</h2>
              <div>
                <a target="_blank" rel="noopener" href="http://ant.design/">
                  Ant Design
                </a>
                <span> - </span>
                <span>蚂蚁 UI 设计体系</span>
              </div>
              <div>
                <a target="_blank" rel="noopener" href="https://eggjs.org/">
                  Egg
                </a>
                <span> - </span>
                <span>企业级 Node Web 开发框架</span>
              </div>
            </div>
          </Col> */}
        </Row>
      </div>
      <Row className="bottom-bar">
        <Col lg={6} sm={24} />
        <Col lg={18} sm={24}>
          <span
            style={{
              lineHeight: "16px",
              paddingRight: 12,
              marginRight: 11,
              borderRight: "1px solid rgba(255, 255, 255, 0.55)",
            }}
          >
            <a
              href="http://www.ensam-umi.ac.ma/"
              rel="noopener noreferrer"
              target="_blank"
            >
              ENSAM Meknès
            </a>
          </span>
          {/* <span style={{ marginRight: 24 }}>
            <a
              href="https://render.alipay.com/p/f/fd-izto3cem/index.html"
              rel="noopener noreferrer"
              target="_blank"
            >
              权益保障承诺书
            </a>
          </span> */}
          {/* <span style={{ marginRight: 12 }}>ICP 证浙 B2-2-100257</span> */}
          <span style={{ marginRight: 12 }}>Copyright © 2023-2024</span>
        </Col>
      </Row>
    </footer>
  );
}

export default Footer;
