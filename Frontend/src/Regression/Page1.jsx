import React, { useState, useEffect } from "react";
import axios from "axios";
import "./static/page1.css";
import { useNavigate } from "react-router-dom";
// import { Layout, Menu } from "antd";
import {
  Layout,
  Menu,
  theme,
  Space,
  Table,
  Tag,
  Checkbox,
  Input,
  Radio,
} from "antd";
import Header from "../Home/Header";

const { Content, Sider } = Layout;
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
    getItem("Processing", "sub1", null, [
      getItem("Cleaning", "1"),
      getItem("Transformation", "2"),
      getItem("Exploration", "3"),
    ]),
    getItem("Exploration", "sub2", null, [
      getItem("Option 3", "4"),
      getItem("Option 4", "5"),
    ]),
    getItem("Machine Leaning", "sub3", null, [
      getItem("Clustering", "6"),
      getItem("Regression", "7"),
      getItem("Classification", "8"),
    ]),
  ];
  let navigate = useNavigate();
  const getstarted = () => {
    navigate("/classification");
  };
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [mycolumns, setMycolumns] = useState(undefined);
  const [mystatisticscolumns, setMystatisticscolumns] = useState(undefined);
  const [cols, setCols] = useState(undefined);
  const [colsLength, setColsLength] = useState(undefined);
  const [rows, setRows] = useState(undefined);
  const [statisticsCols, setStatisticsCols] = useState(undefined);
  const [statisticsColsLength, setStatisticsColsLength] = useState(undefined);
  const [statisticsRows, setStatisticsRows] = useState(undefined);

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    console.log(e.target.files);
    if (file != null) {
      const data = new FormData();
      data.append("file", file);

      await axios
        .post("/upload", data)
        .then(async function (response) {
          if (response.data == "Uploaded") {
            window.dialog.close();
          }
          console.log(response);
          await axios
            .get("/getrows")
            .then(function (response) {
              let myrows = response.data;
              setRows(myrows);
              console.log(rows);
            })
            .catch(function (error) {
              console.log(error);
            });

          await axios
            .get("/getcols")
            .then(function (response) {
              setCols(response.data["columns"].filter((e) => e !== "index"));
              setColsLength(
                response.data["columns"].filter((e) => e !== "index").length
              );
            })
            .catch(function (error) {
              console.log(error);
            });
          await axios
            .get("/getstatisticsrows")
            .then(async function (response) {
              setStatisticsRows(response.data);
              await axios
                .get("/getstatisticscols")
                .then(function (response) {
                  setStatisticsCols(
                    response.data["columns"].filter((e) => e !== "index")
                  );
                  setStatisticsColsLength(
                    response.data["columns"].filter((e) => e !== "index").length
                  );
                  // document.getElementById("statisticsdata").style.top =
                  //   document.getElementById("mydata").clientHeight;
                  // console.log(statisticsColsLength);
                })
                .catch(function (error) {
                  console.log(error);
                });
            })
            .catch(function (error) {
              console.log(error);
            });
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  };
  useEffect(() => {
    const updatedColumns = [];

    for (let index = 0; index < colsLength; index++) {
      const addCols = {
        title: cols[index],
        dataIndex: cols[index],
      };
      updatedColumns.push(addCols);
    }

    console.log("Columns updated:", updatedColumns);
    // Update the state variable 'mycolumns'
    setMycolumns(updatedColumns);

    const updatedStatisticsColumns = [];

    for (let index = 0; index < statisticsColsLength; index++) {
      const addStatisticsCols = {
        title: statisticsCols[index],
        dataIndex: statisticsCols[index],
      };
      updatedStatisticsColumns.push(addStatisticsCols);
    }

    console.log("Columns updated:", updatedStatisticsColumns);
    // Update the state variable 'mycolumns'
    setMystatisticscolumns(updatedStatisticsColumns);
  }, [cols, colsLength, statisticsCols, statisticsColsLength]);

  const data = rows;
  const statisticsdata = statisticsRows;
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);
  const [loading, setLoading] = useState(false);
  const start = () => {
    setLoading(true);
    // ajax request after empty completing
    setTimeout(() => {
      setSelectedRowKeys([]);
      setLoading(false);
    }, 1000);
  };
  const onSelectChange = (newSelectedRowKeys) => {
    console.log("selectedRowKeys changed: ", newSelectedRowKeys);
    setSelectedRowKeys(newSelectedRowKeys);
  };
  const rowSelection = {
    selectedRowKeys,
    onChange: onSelectChange,
  };
  const hasSelected = selectedRowKeys.length > 0;

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
      // window.dialog.close();
      return () => {
        dialogElement.removeEventListener("close", handleDialogClose);
      };
    }
  }, []);
  const [selectedKey, setSelectedKey] = useState(["1"]);
  const [firstPage, setFirstPage] = useState(true);
  const [secondPage, setSecondPage] = useState(false);
  const [thirdPage, setThirdPage] = useState(false);
  const [forthPage, setForthPage] = useState(false);
  const [sixthPage, setSixthPage] = useState(false);
  const onClick = async (e) => {
    console.log(e.key);
    setSelectedKey([e.key]);
    console.log(e);
    if (e.key == 1) {
      setFirstPage(true);
      setSecondPage(false);
      setThirdPage(false);
      setForthPage(false);
      setSixthPage(false);
    }
    if (e.key == 2) {
      setFirstPage(false);
      setSecondPage(true);
      setThirdPage(false);
      setForthPage(false);
      setSixthPage(false);
    }
    if (e.key == 3) {
      setFirstPage(false);
      setSecondPage(false);
      setThirdPage(true);
      setForthPage(false);
      setSixthPage(false);
    }
    if (e.key == 4) {
      setFirstPage(false);
      setSecondPage(false);
      setThirdPage(false);
      setForthPage(true);
      setSixthPage(false);
    }
    if (e.key == 6) {
      setFirstPage(false);
      setSecondPage(false);
      setThirdPage(false);
      setForthPage(false);
      setSixthPage(true);
    }
  };
  // const onChange = (checkedValues) => {
  //   console.log("checked = ", checkedValues);
  // };

  const options = [
    {
      label: "Apple",
      value: "Apple",
    },
    {
      label: "Pear",
      value: "Pear",
    },
    {
      label: "Orange",
      value: "Orange",
    },
  ];

  const [value, setValue] = useState(1);
  const onChange = (e) => {
    console.log("radio checked", e.target.value);
    setValue(e.target.value);
  };

  const clusterMethod = () => {
    axios.post("/get_visualisation", data).then(function (res) {
      console.log(res);
    });
  };

  return (
    <div>
      <Layout>
        <Header />
        <Layout style={{ paddingTop: "64px" }}>
          <Sider
            width={230}
            style={{
              background: "#f8fafe",
              // position: "fixed",
            }}
          >
            <Menu
              mode="inline"
              defaultSelectedKeys={["1"]}
              selectedKeys={selectedKey}
              defaultOpenKeys={["sub1"]}
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
            {firstPage ? (
              <Space
                direction="vertical"
                size="middle"
                style={{ display: "flex" }}
              >
                {cols !== undefined ? (
                  <Content
                    style={{
                      padding: 24,
                      margin: 0,
                      minHeight: 80,
                      background: colorBgContainer,
                      borderRadius: borderRadiusLG,
                    }}
                  >
                    <h5>Your Data</h5>
                    <div>
                      <div
                        style={{
                          marginBottom: 16,
                        }}
                      >
                        <span
                          style={{
                            marginLeft: 8,
                          }}
                        >
                          {hasSelected
                            ? `Selected ${selectedRowKeys.length} items`
                            : ""}
                        </span>
                      </div>
                      <Table
                        rowSelection={rowSelection}
                        columns={mycolumns}
                        dataSource={data}
                        scroll={{
                          x: 1300,
                        }}
                        size="small"
                      />
                    </div>
                  </Content>
                ) : (
                  ""
                )}
                {statisticsCols !== undefined ? (
                  <div className="row">
                    <div className="col-6">
                      <Content
                        style={{
                          padding: 24,
                          margin: 0,
                          minHeight: 80,
                          background: colorBgContainer,
                          borderRadius: borderRadiusLG,
                        }}
                      >
                        <h5>Statistics on your Data</h5>
                        <div>
                          <div
                            style={{
                              marginBottom: 16,
                            }}
                          >
                            <span
                              style={{
                                marginLeft: 8,
                              }}
                            >
                              {hasSelected
                                ? `Selected ${selectedRowKeys.length} items`
                                : ""}
                            </span>
                          </div>
                          <Table
                            rowSelection={rowSelection}
                            columns={mystatisticscolumns}
                            dataSource={statisticsdata}
                            size="small"
                          />
                        </div>
                      </Content>
                    </div>
                    <div className="col-6">
                      <Content
                        style={{
                          padding: 24,
                          margin: 0,
                          minHeight: 80,
                          background: colorBgContainer,
                          borderRadius: borderRadiusLG,
                        }}
                      >
                        <h5>Cleaning</h5>
                        <Checkbox.Group
                          options={options}
                          defaultValue={["Pear"]}
                          onChange={onChange}
                        />
                      </Content>
                    </div>
                  </div>
                ) : (
                  ""
                )}
              </Space>
            ) : (
              ""
            )}
            {secondPage ? (
              <Content
                style={{
                  padding: 24,
                  margin: 0,
                  minHeight: 80,
                  background: colorBgContainer,
                  borderRadius: borderRadiusLG,
                }}
              >
                <h5>Transformation</h5>
              </Content>
            ) : (
              ""
            )}
            {sixthPage ? (
              <div className="row">
                <div className="col-6">
                  <Content
                    style={{
                      padding: 24,
                      margin: 0,
                      minHeight: 80,
                      background: colorBgContainer,
                      borderRadius: borderRadiusLG,
                    }}
                  >
                    <h5>Optimal number of clusters</h5>
                    <form action="submit" name="clusterMethod">
                      <Radio.Group onChange={onChange} value={value}>
                        <Space direction="vertical">
                          <Radio value={"elbow"}>
                            Use Elbow Method
                            {value == 1 ? (
                              <div>
                                <Input
                                  style={{
                                    width: 100,
                                    marginLeft: 10,
                                  }}
                                  placeholder="min_clusters"
                                />
                                <Input
                                  style={{
                                    width: 100,
                                    marginLeft: 10,
                                  }}
                                  placeholder="max_clusters"
                                />
                              </div>
                            ) : null}
                          </Radio>
                          <Radio value={"silhouette"}>
                            Use Silhouette Method
                            {value == 2 ? (
                              <div>
                                <Input
                                  style={{
                                    width: 100,
                                    marginLeft: 10,
                                  }}
                                  placeholder="min_clusters"
                                />
                                <Input
                                  style={{
                                    width: 100,
                                    marginLeft: 10,
                                  }}
                                  placeholder="max_clusters"
                                />
                              </div>
                            ) : null}
                          </Radio>
                          <Radio value={"dendrogram"}>
                            Use Dendrogram Method
                          </Radio>
                        </Space>
                      </Radio.Group>
                    </form>
                    <button className="btn btn-primary" id="submit">
                      Submit
                    </button>
                  </Content>
                </div>
                <div className="col-6">
                  <Content
                    style={{
                      padding: 24,
                      margin: 0,
                      minHeight: 80,
                      background: colorBgContainer,
                      borderRadius: borderRadiusLG,
                    }}
                  >
                    <h5>Clustering</h5>
                  </Content>
                </div>
              </div>
            ) : (
              ""
            )}
          </Layout>
        </Layout>
      </Layout>
      <div>
        <dialog id="dialog">
          <div>
            <div className="flex flex-col items-center justify-center w-full h-full">
              <div className="mt-10 mb-10 text-center">
                <h2 className="text-2xl font-semibold mb-2">
                  Upload your files
                </h2>
                <p className="text-xs text-gray-500">
                  File should be of format .csv, .xlsx or .xls
                </p>
              </div>
              <form
                action="#"
                className="relative w-4/5 h-32 max-w-xs mb-10 bg-white bg-gray-100 rounded-lg shadow-inner"
                encType="multipart/form-data"
              >
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  multiple="multiple"
                  onChange={uploadFile}
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
            </div>
          </div>
        </dialog>
      </div>
    </div>
  );
}

export default Page1;
