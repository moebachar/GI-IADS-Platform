import React, { useState, useEffect, useRef } from "react";
import "./static/page1.css";
import { useNavigate } from "react-router-dom";
// import { Layout, Menu } from "antd";
import { Breadcrumb, Layout, Menu, theme } from "antd";
import { Space } from "antd";
import Header from "../Home/Header";
import explainingImage from "./static/explaining_classification.png";
import "./static/page2.css";
import axios from "axios";
import BarChart from "../components_jsx/bar_chart";
import CardModel from "../components_jsx/Card_model";
import { Card, Col, Row } from "antd";

const { Content, Sider } = Layout;
const { Meta } = Card;
function Page1() {
  function getItem(label, key, icon, children, type) {
    return {
      key,
      icon,
      children,
      label,
      type,
    };
  }
  const items = [
    getItem("Exploration", "1", null, null),
    getItem("Model", "sub2", null, [
      getItem("Build a Model", "2"),
      getItem("Upload a Model", "3"),
      getItem("Choose a Pretrained Model", "4"),
    ]),
    getItem("Item3", "sub3", null, null),
  ];
  let navigate = useNavigate();
  const getstarted = () => {
    navigate("/classification");
  };
  const [showFirstDiv, setShowFirstDiv] = useState(true);
  const [showSecondDiv, setShowSecondDiv] = useState(false);
  const [showThirdDiv, setShowThirdDiv] = useState(false);
  const [showForthDiv, setShowForthDiv] = useState(false);
  const [dialogStyle, setDialogStyle] = useState({
    width: "400px",
    height: "200px",
  });
  // const [files, setFiles] = useState([]);
  const [classes, setClasses] = useState(["1", "2"]);
  const [inputMessage, setInputMessage] = useState(
    Array(classes.length).fill("")
  );
  const [spanBackgroundColors, setSpanBackgroundColors] = useState(
    Array(classes.length).fill("badge rounded-pill text-bg-warning")
  );
  const [showAlert, setShowAlert] = useState(false);
  const [showError, setShowError] = useState(false);
  const [animationClassName, setAnimationClassName] = useState(
    "animated-div-forward"
  );

  const addClasses = () => {
    let pushNumber = classes.length + 1;
    const newClasses = [...classes, pushNumber.toString()];
    setClasses(newClasses);
    setShowAlert(false);
    setSpanBackgroundColors([
      ...spanBackgroundColors,
      "badge rounded-pill text-bg-warning",
    ]);
    setInputMessage([...inputMessage, ""]);
    let addHeight = (classes.length - 2) * 48 + 338;
    setDialogStyle({ width: "500px", height: addHeight.toString() + "px" });
  };
  const handleDialogOpen = () => {
    // Logic to execute when the dialog opens
    console.log("Dialog opened");
  };

  const handleDialogClose = () => {
    // Logic to execute when the dialog closes
    console.log("Dialog closed");
  };

  useEffect(() => {
    const dialogElement = document.getElementById("dialog");

    // Check if the dialog element exists
    if (dialogElement) {
      // Use showModal to open the dialog (which also creates the backdrop)
      dialogElement.showModal();

      // Attach event listeners
      dialogElement.addEventListener("close", handleDialogClose);

      // Cleanup: Remove event listeners when the component unmounts
      return () => {
        dialogElement.removeEventListener("close", handleDialogClose);
      };
    }
  }, []);

  const handleInputMessage = (index, e) => {
    const updatedColors = [...spanBackgroundColors];
    const updatedInputMessages = [...inputMessage];
    updatedInputMessages[index] = e.target.value;
    setInputMessage(updatedInputMessages);
    setShowAlert(false);

    if (e.target.value === "") {
      updatedColors[index] = "badge rounded-pill text-bg-warning";
    } else {
      updatedColors[index] = "badge rounded-pill text-bg-primary";
    }

    console.log(index);
    setSpanBackgroundColors(updatedColors);
  };

  const handleDeleteClass = (index) => {
    if (classes.length <= 2) {
      setShowAlert(true);
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
      return;
    } else {
      setShowAlert(false);
    }
    let updatedClasses = [...classes];
    updatedClasses.splice(index, 1);
    setClasses(updatedClasses);

    let updatedColors = [...spanBackgroundColors];
    updatedColors.splice(index, 1);
    setSpanBackgroundColors(updatedColors);

    let updatedInputMessages = [...inputMessage];
    updatedInputMessages.splice(index, 1);
    setInputMessage(updatedInputMessages);

    let reduceHeight = (classes.length - 3) * 48 + 290;
    setDialogStyle({ width: "500px", height: reduceHeight.toString() + "px" });
  };

  const resetClasses = () => {
    console.log("Before setClasses", classes);
    setClasses(["1", "2"]);
    console.log("After setClasses", classes);

    let updatedInputMessages = Array(classes.length).fill("");
    setInputMessage(["", ""]);

    let updatedColors = Array(classes.length).fill(
      "badge rounded-pill text-bg-warning"
    );
    setSpanBackgroundColors(updatedColors);

    setDialogStyle({ width: "500px", height: "290px" });
  };

  const newImport = () => {
    setDialogStyle({ width: "600px", height: "450px" });
    setShowFirstDiv(!showFirstDiv);
    setShowSecondDiv(!showSecondDiv);
  };

  const backImport = () => {
    setDialogStyle({ width: "400px", height: "200px" });
    setAnimationClassName("animated-div-backward");
    setShowFirstDiv(!showFirstDiv);
    setShowSecondDiv(!showSecondDiv);
  };

  const createDataset = () => {
    let addHeight = (classes.length - 3) * 48 + 338;
    setDialogStyle({ width: "500px", height: addHeight.toString() + "px" });
    setAnimationClassName("animated-div-forward");
    setShowFirstDiv(!showFirstDiv);
    setShowThirdDiv(!showThirdDiv);
  };

  const backCreateData = () => {
    setDialogStyle({ width: "400px", height: "200px" });
    setAnimationClassName("animated-div-backward");
    setShowFirstDiv(!showFirstDiv);
    setShowThirdDiv(!showThirdDiv);
  };

  const nextUpload = () => {
    let indexArray;
    for (let index = 0; index < classes.length; index++) {
      if (inputMessage[index].trim() === "") {
        setShowError(true);
        setTimeout(() => {
          setShowError(false);
        }, 3000);
        return;
      }
    }
    let nextUploadHeight = 165 + inputMessage.length * 139.2;
    if (nextUploadHeight < 722) {
      setDialogStyle({
        width: "500px",
        height: nextUploadHeight.toString() + "px",
      });
    } else {
      setDialogStyle({
        width: "500px",
        height: "600px",
        overflowY: "scroll",
      });
    }

    setShowThirdDiv(!showThirdDiv);
    setShowForthDiv(!showForthDiv);
    console.log(inputMessage);
    axios
      .post("/Create_data_I", { class_names: inputMessage })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const backCreateClass = () => {
    let addHeight = (classes.length - 3) * 48 + 338;
    setDialogStyle({ width: "500px", height: addHeight.toString() + "px" });
    setAnimationClassName("animated-div-backward");
    setShowThirdDiv(!showThirdDiv);
    setShowForthDiv(!showForthDiv);
  };

  const [firstPage, setFirstPage] = useState(true);
  const [secondPage, setSecondPage] = useState(false);
  const [thirdPage, setThirdPage] = useState(false);
  const [forthPage, setForthPage] = useState(false);

  const [selectedKey, setSelectedKey] = useState(["1"]);
  const onClick = async (e) => {
    setSelectedKey([e.key]);
    console.log(e);
    if (e.key == 1) {
      setFirstPage(true);
      setSecondPage(false);
      setThirdPage(false);
      setForthPage(false);
    }
    if (e.key == 2) {
      setFirstPage(false);
      setSecondPage(true);
      setThirdPage(false);
      setForthPage(false);
    }
    if (e.key == 3) {
      setFirstPage(false);
      setSecondPage(false);
      setThirdPage(true);
      setForthPage(false);
    }
    if (e.key == 4) {
      setFirstPage(false);
      setSecondPage(false);
      setThirdPage(false);
      setForthPage(true);
    }
  };

  const buildModel = () => {
    setSelectedKey(["2"]);
    setFirstPage(false);
    setSecondPage(true);
    setThirdPage(false);
    setForthPage(false);
  };
  const uploadModel = () => {
    setSelectedKey(["3"]);
    setFirstPage(false);
    setSecondPage(false);
    setThirdPage(true);
    setForthPage(false);
  };
  const pretrainedModel = () => {
    setSelectedKey(["4"]);
    setFirstPage(false);
    setSecondPage(false);
    setThirdPage(false);
    setForthPage(true);
  };

  useEffect(() => console.log(firstPage), [firstPage]);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  // useEffect(() => {

  const appendFile = (index) => {
    console.log(index);
    console.log("hello");
    // const file = event.target.files;
    // console.log(file);
    // let name = "file" + index.toString();
    // data.append(name, file);
  };
  // const file = event.target.files;

  // for (let i = 0; i < file.length; i++) {
  //   let name = "file" + index.toString();
  //   data.append(name, file[i]);
  // }
  // };
  // }, []);
  // let appendFile = (index, e) => {
  //   const file = e.target.files;
  //   console.log(index);

  //   // for (let i = 0; i < file.length; i++) {
  //   //   let name = "file" + index.toString();
  //   //   data.append(name, file[i]);
  //   // }
  // };

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    const mydata = new FormData();
    if (file != null) {
      mydata.append("file", file);
      console.log(mydata);
    }
    axios
      .post("/Import_dataset", mydata)
      .then(function (response) {
        if (response.data["status"] === "successful") {
          window.dialog.close();
        }
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const data = new FormData();

  const handleFileChange = (index, event) => {
    console.log("Index:", index);
    console.log("Files:", event.target.files);
    const file = event.target.files;
    for (let i = 0; i < file.length; i++) {
      data.append("file" + index.toString(), file[i]);
    }

    // Update the files state with the selected files for the current index
    // const newFiles = [...files];
    // newFiles[index] = event.target.files;
    // setFiles(newFiles);
  };

  const [height, setHeight] = useState([]);
  const [width, setWidth] = useState([]);
  const sendFiles = () => {
    axios
      .post("/Create_data_II", data)
      .then(function (response) {
        if (response.data["status"] == "redirect") {
          window.dialog.close();
        }
        axios
          .get("/Exploration")
          .then(function (response) {
            setWidth(response.data["items"][4]);
            setHeight(response.data["items"][5]);
          })
          .catch(function (error) {
            console.log(error);
          });
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };
  useEffect(() => {
    console.log(width);
    console.log(height);
  }, [width, height]);

  const [inputLayer, setInputLayer] = useState([224, 224]);
  const [convLayer, setConvLayer] = useState([32, 3, 3]);
  const [poolLayer, setPoolLayer] = useState([2, 2]);
  const [poolingLayers, setPoolingLayers] = useState([]);

  const handleInputLayer = (event, index) => {
    const newValues = [...inputLayer];
    newValues[index] = event.target.value;
    setInputLayer(newValues);
  };

  const handleConvLayer = (event, index) => {
    const newValues = [...convLayer];
    newValues[index] = event.target.value;
    setConvLayer(newValues);
  };

  const handlePoolLayer = (event, index) => {
    const newValues = [...poolLayer];
    newValues[index] = event.target.value;
    setPoolLayer(newValues);
  };

  const addMaxPoolingLayer = () => {
    // Add a new pooling layer to the collection
    const newPoolingLayer = [2, 2]; // You can customize this value
    setPoolingLayers([...poolingLayers, newPoolingLayer]);
  };

  useEffect(() => {
    console.log(poolingLayers);
  });

  return (
    <div>
      <Layout>
        <Header />
        <Layout style={{ paddingTop: "64px" }}>
          <Sider
            width={200}
            style={{
              background: "#f8fafe",
            }}
          >
            <Menu
              mode="inline"
              defaultSelectedKeys={["1"]}
              selectedKeys={selectedKey}
              defaultOpenKeys={["1"]}
              style={{
                height: "100vh",
                borderRight: 0,
                background: "#f8fafe",
                bottom: 0,
              }}
              items={items}
              onClick={onClick}
            />
          </Sider>
          <Layout
            style={{
              padding: "10px 24px 24px",
            }}
          >
            <Space
              direction="vertical"
              size="middle"
              style={{ display: "flex" }}
            >
              {firstPage && inputMessage !== Array(classes.length).fill("") ? (
                <div className="fadein">
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ display: "flex" }}
                  >
                    <div className="row" id="scroll-div">
                      <Space
                        direction="horizantal"
                        size="middle"
                        style={{ display: "flex" }}
                      >
                        {inputMessage.map((inputItem, index) => (
                          <div className="col" key={index}>
                            <Content
                              style={{
                                padding: 24,
                                margin: 0,
                                minHeight: 80,
                                background: colorBgContainer,
                                borderRadius: borderRadiusLG,
                              }}
                            >
                              <h6>
                                Class <strong>{inputItem}</strong>{" "}
                              </h6>
                              <BarChart
                                key={index}
                                width={width[index]}
                                height={height[index]}
                              />
                            </Content>
                          </div>
                        ))}
                      </Space>
                    </div>

                    <Row gutter={16}>
                      <Col span={8}>
                        <Card
                          style={{
                            cursor: "pointer",
                          }}
                          onClick={buildModel}
                        >
                          <Meta title="Build your own model" />
                        </Card>
                      </Col>
                      <Col span={8}>
                        <Card
                          style={{
                            cursor: "pointer",
                          }}
                          onClick={uploadModel}
                        >
                          <Meta title="Upload your Model (h5 or zip)" />
                        </Card>
                      </Col>
                      <Col span={8}>
                        <Card
                          style={{
                            cursor: "pointer",
                          }}
                          onClick={pretrainedModel}
                        >
                          <Meta title="Choose a Pretrained Model (MobileNet...)" />
                        </Card>
                      </Col>
                    </Row>
                  </Space>
                </div>
              ) : (
                ""
              )}
              {secondPage ? (
                <div className="fadein">
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ display: "flex" }}
                  >
                    <Content
                      style={{
                        padding: 24,
                        margin: 0,
                        minHeight: 80,
                        background: colorBgContainer,
                        borderRadius: borderRadiusLG,
                      }}
                    >
                      <div>
                        <h4>Build Your Own model</h4>
                        <div className="layer-input-layer">
                          <h3 className="input-layer">Input Layer</h3>
                          <div className="row">
                            <label htmlFor="inputFilterHeightInp">
                              Input Height:
                            </label>
                            <div style={{ width: "150px", margin: "auto" }}>
                              <input
                                type="number"
                                id="inputFilterHeightInp"
                                className="form-control"
                                name="inputFilterHeightInp"
                                min="0"
                                max="1000"
                                value={inputLayer[0]}
                                onChange={(e) => handleInputLayer(e, 0)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                          <div className="row" style={{ paddingTop: "5px" }}>
                            <label htmlFor="inputFilterWidthInp">
                              Input Width:
                            </label>
                            <div
                              style={{
                                width: "150px",
                                margin: "auto",
                                paddingBottom: "10px",
                              }}
                            >
                              <input
                                type="number"
                                className="form-control"
                                id="inputFilterWidthInp"
                                name="inputFilterWidthInp"
                                min="0"
                                max="1000"
                                value={inputLayer[1]}
                                onChange={(e) => handleInputLayer(e, 1)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                        </div>
                        <div className="layer-conv-layer">
                          <h3 className="input-layer">Convolutional Layer</h3>
                          <div className="row">
                            <label htmlFor="inputFilterHeightInp">
                              Number of filters
                            </label>
                            <div style={{ width: "150px", margin: "auto" }}>
                              <input
                                type="number"
                                id="inputFilterHeightInp"
                                className="form-control"
                                name="inputFilterHeightInp"
                                min="0"
                                max="1000"
                                value={convLayer[0]}
                                onChange={(e) => handleConvLayer(e, 0)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                          <div className="row" style={{ paddingTop: "5px" }}>
                            <label htmlFor="inputFilterWidthInp">
                              Filter Height:
                            </label>
                            <div
                              style={{
                                width: "150px",
                                margin: "auto",
                              }}
                            >
                              <input
                                type="number"
                                className="form-control"
                                id="inputFilterWidthInp"
                                name="inputFilterWidthInp"
                                min="0"
                                max="1000"
                                value={convLayer[1]}
                                onChange={(e) => handleConvLayer(e, 1)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                          <div className="row" style={{ paddingTop: "5px" }}>
                            <label htmlFor="inputFilterWidthInp">
                              Filter Width:
                            </label>
                            <div
                              style={{
                                width: "150px",
                                margin: "auto",
                                paddingBottom: "10px",
                              }}
                            >
                              <input
                                type="number"
                                className="form-control"
                                id="inputFilterWidthInp"
                                name="inputFilterWidthInp"
                                min="0"
                                max="1000"
                                value={convLayer[2]}
                                onChange={(e) => handleConvLayer(e, 2)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                        </div>
                        <div className="layer-maxpool-layer">
                          <h3 className="input-layer">MaxPooling Layer</h3>
                          <div className="row">
                            <label htmlFor="inputFilterHeightInp">
                              Pool Height
                            </label>
                            <div style={{ width: "150px", margin: "auto" }}>
                              <input
                                type="number"
                                id="inputFilterHeightInp"
                                className="form-control"
                                name="inputFilterHeightInp"
                                min="0"
                                max="1000"
                                value={poolLayer[0]}
                                onChange={(e) => handlePoolLayer(e, 0)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                          <div className="row" style={{ paddingTop: "5px" }}>
                            <label htmlFor="inputFilterWidthInp">
                              Pool Width
                            </label>
                            <div
                              style={{
                                width: "150px",
                                margin: "auto",
                              }}
                            >
                              <input
                                type="number"
                                className="form-control"
                                id="inputFilterWidthInp"
                                name="inputFilterWidthInp"
                                min="0"
                                max="1000"
                                value={poolLayer[1]}
                                onChange={(e) => handlePoolLayer(e, 1)}
                                style={{
                                  width: "150px",
                                  borderRadius: "20px",
                                  height: "30px",
                                }}
                              />
                            </div>
                          </div>
                        </div>
                        {poolingLayers.map((poolLayerItem, index) => {
                          <div className="layer-maxpool-layer">
                            <h3 className="input-layer">MaxPooling Layer</h3>
                            <div className="row">
                              <label htmlFor="inputFilterHeightInp">
                                Pool Height
                              </label>
                              <div style={{ width: "150px", margin: "auto" }}>
                                <input
                                  type="number"
                                  id="inputFilterHeightInp"
                                  className="form-control"
                                  name="inputFilterHeightInp"
                                  min="0"
                                  max="1000"
                                  value={poolLayer[0]}
                                  onChange={(e) => handlePoolLayer(e, 0)}
                                  style={{
                                    width: "150px",
                                    borderRadius: "20px",
                                    height: "30px",
                                  }}
                                />
                              </div>
                            </div>
                            <div className="row" style={{ paddingTop: "5px" }}>
                              <label htmlFor="inputFilterWidthInp">
                                Pool Width
                              </label>
                              <div
                                style={{
                                  width: "150px",
                                  margin: "auto",
                                }}
                              >
                                <input
                                  type="number"
                                  className="form-control"
                                  id="inputFilterWidthInp"
                                  name="inputFilterWidthInp"
                                  min="0"
                                  max="1000"
                                  value={poolLayer[1]}
                                  onChange={(e) => handlePoolLayer(e, 1)}
                                  style={{
                                    width: "150px",
                                    borderRadius: "20px",
                                    height: "30px",
                                  }}
                                />
                              </div>
                            </div>
                          </div>;
                        })}
                        <div
                          className="row"
                          style={{ margin: "auto", width: "50%" }}
                        >
                          <div className="col" id="col">
                            <button
                              className="btn btn-primary"
                              onClick={addMaxPoolingLayer}
                            >
                              Add MaxPooling
                            </button>
                          </div>
                          <div className="col" id="col">
                            <button className="btn btn-primary">
                              Add Conv 2d{" "}
                            </button>
                          </div>
                          <div className="col" id="col">
                            <button className="btn btn-light">
                              Drop Last Layer
                            </button>
                          </div>
                        </div>
                      </div>
                    </Content>
                  </Space>
                </div>
              ) : (
                ""
              )}
              {thirdPage ? (
                <div className="fadein">
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ display: "flex" }}
                  >
                    <Content
                      style={{
                        padding: 24,
                        margin: 0,
                        minHeight: 80,
                        background: colorBgContainer,
                        borderRadius: borderRadiusLG,
                      }}
                    >
                      <h4>Upload a model</h4>
                    </Content>
                  </Space>
                </div>
              ) : (
                ""
              )}
              {forthPage ? (
                <div className="fadein">
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ display: "flex" }}
                  >
                    <Content
                      style={{
                        padding: 24,
                        margin: 0,
                        minHeight: 80,
                        background: colorBgContainer,
                        borderRadius: borderRadiusLG,
                      }}
                    >
                      <h4>Pretrained Model</h4>
                    </Content>
                  </Space>
                </div>
              ) : (
                ""
              )}
            </Space>
          </Layout>
        </Layout>
      </Layout>
      <div>
        {/* {openDialog && ( */}
        <dialog id="dialog" style={dialogStyle}>
          <div>
            {showFirstDiv ? (
              <div className={animationClassName}>
                <h3 id="text">How would you like to enter your dataset?</h3>
                <div className="row" id="firstdivrow">
                  <div className="col col-6 ms-3">
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={createDataset}
                      id="btn"
                    >
                      Create a new dataset
                    </button>
                  </div>
                  <div className="col ms-4">
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={newImport}
                      id="btn"
                    >
                      Import Dataset
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              ""
            )}
            {showSecondDiv ? (
              <div className="animated-div-forward">
                <h5 id="text">
                  Your dataset should consist of a dedicated file for each
                  class, and within each file, you will find the data
                  corresponding to that class
                </h5>
                <img
                  src={explainingImage}
                  alt=""
                  style={{
                    display: "block",
                    marginLeft: "auto",
                    marginRight: "auto",
                    width: "95%",
                  }}
                />
                <h5 id="text">Import a .zip file</h5>
                <form
                  action="#"
                  className="relative w-full h-32 bg-slate-100 bg-gray-100 rounded-lg shadow-inner"
                  encType="multipart/form-data"
                >
                  <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    onChange={uploadFile} //DONE
                    // name="file"
                  />
                  <label
                    htmlFor="file-upload"
                    className="z-20 flex flex-col-reverse items-center justify-center w-full h-full cursor-pointer"
                  >
                    <p className="z-10 text-xs font-light text-center text-gray-500">
                      Drag & Drop your files here
                    </p>
                    <svg
                      className="z-10 w-8 h-8 text-indigo-400"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"></path>
                    </svg>
                  </label>
                </form>
                <button
                  className="btn btn-light"
                  style={{ marginTop: "10px", float: "right" }}
                  id="back-btn"
                  onClick={backImport}
                >
                  Back
                </button>
              </div>
            ) : (
              ""
            )}
            {showThirdDiv ? (
              <div className={animationClassName}>
                <h5 id="text">Enter the name of your classes</h5>
                <div className="row" id="classrow">
                  <div className="col-5">
                    <button className="btn btn-primary" onClick={addClasses}>
                      Add classes
                    </button>
                  </div>
                  <div className="col offset-ms-1">
                    <button className="btn btn-light" onClick={resetClasses}>
                      Reset
                    </button>
                  </div>
                </div>

                {classes.map((classItem, index) => (
                  <div className="row" id="inputrow" key={index}>
                    <div className="col-2" id="col-2">
                      <span
                        className={spanBackgroundColors[index]}
                        id="basic-addon1"
                      >
                        Class{classItem}
                      </span>
                    </div>
                    <div className="col">
                      <input
                        type="text"
                        value={inputMessage[index]}
                        className="form-control"
                        placeholder="Class Name"
                        aria-label="Class Name"
                        aria-describedby="basic-addon1"
                        id="text-input"
                        onChange={(event) => handleInputMessage(index, event)}
                      />
                    </div>
                    <div className="col">
                      <button
                        className="btn"
                        onClick={() => handleDeleteClass(index)}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          fill="currentColor"
                          className="bi bi-trash"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                          <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
                {showAlert && (
                  <div
                    className="alert alert-warning alert-dismissible fade show"
                    role="alert"
                    id="alert"
                  >
                    <strong id="strong">
                      The mininum classes needed is two
                    </strong>
                  </div>
                )}
                {showError && (
                  <div
                    className="alert alert-danger alert-dismissible fade show"
                    role="alert"
                    id="alert"
                  >
                    <strong id="strong">
                      Please fill all the fields before submitting
                    </strong>
                  </div>
                )}
                <div>
                  <button
                    className="btn btn-primary inline"
                    id="next-btn"
                    style={{ marginTop: "15px", float: "right" }}
                    onClick={nextUpload}
                  >
                    Next
                  </button>
                  <button
                    className="btn btn-light inline"
                    id="next-btn"
                    style={{
                      marginTop: "15px",
                      float: "right",
                      marginInlineEnd: "10px",
                    }}
                    onClick={backCreateData}
                  >
                    Back
                  </button>
                </div>
              </div>
            ) : (
              ""
            )}
            {showForthDiv ? (
              <div className="animated-div-forward">
                <h5 id="text">Enter the data for each class</h5>
                <h6
                  id="text"
                  style={{
                    fontStyle: "italic",
                    fontSize: "15px",
                  }}
                >
                  Your data must be images or tabular files containing URLs
                </h6>
                <form
                  className=""
                  encType="multipart/form-data"
                  id="input-create-data"
                >
                  {inputMessage.map((inputItem, currentIndex) => {
                    return (
                      <div key={inputItem.id}>
                        <h6>
                          Enter your data for the class{" "}
                          <strong> {inputItem}</strong>
                        </h6>
                        <div className="relative h-28 bg-slate-100 bg-gray-100 rounded-lg shadow-inner">
                          <input
                            type="file"
                            id={`file-upload-${currentIndex}`}
                            className="hidden"
                            multiple="multiple"
                            onChange={(event) =>
                              handleFileChange(currentIndex, event)
                            }
                          />
                          <label
                            htmlFor={`file-upload-${currentIndex}`}
                            className="z-20 flex flex-col-reverse items-center justify-center w-full h-full cursor-pointer"
                          >
                            <p className="z-10 text-xs font-light text-center text-gray-500">
                              Drag & Drop your files here
                            </p>
                            <svg
                              className="z-10 w-8 h-8 text-indigo-400"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"></path>
                            </svg>
                          </label>
                        </div>
                      </div>
                    );
                  })}
                </form>
                <div>
                  <button
                    className="btn btn-primary inline"
                    id="next-btn"
                    style={{ marginTop: "15px", float: "right" }}
                    onClick={sendFiles}
                  >
                    Submit
                  </button>
                  <button
                    className="btn btn-light inline"
                    id="next-btn"
                    style={{
                      marginTop: "15px",
                      float: "right",
                      marginInlineEnd: "10px",
                    }}
                    onClick={backCreateClass}
                  >
                    Back
                  </button>
                </div>
              </div>
            ) : (
              ""
            )}
          </div>
        </dialog>
      </div>
    </div>
  );
}

export default Page1;
