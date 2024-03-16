import React from "react";
import Header from "../Home/Header";
import Page1 from "./Page1";
import DocumentTitle from "react-document-title";
import { enquireScreen } from "enquire-js";
import "./static/page1.css"; // Import your styles

let isMobile = false;
enquireScreen((b) => {
  isMobile = b;
});

class Regression extends React.PureComponent {
  state = {
    isMobile,
    showShadow: false,
  };

  componentDidMount() {
    enquireScreen((b) => {
      this.setState({
        isMobile: !!b,
      });
    });
  }
  navToShadow = (e) => {
    this.setState({ showShadow: e.mode === "leave" });
  };

  render() {
    return [
      <Page1 key="page1" />,
      <DocumentTitle title="GI-IADS Platform" key="doctitle" />,
    ];
  }
}

export default Regression;
