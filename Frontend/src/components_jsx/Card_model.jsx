import React, { useState } from "react";
import { Card } from "antd";
import BarChart from "./bar_chart";
import BuildModel from "./build";

const tabList = [
  {
    key: "tab1",
    tab: "Build your own model",
  },
  {
    key: "tab2",
    tab: "Upload your Model (h5 or zip)",
  },
  {
    key: "tab3",
    tab: "Choose a Pretrained Model (MobileNet...)",
  },
];

const contentList = {
  tab1: <BuildModel />,
  tab2: <p>content2</p>,
  tab3: <p>content3</p>,
};

function CardModel() {
  const [activeTabKey1, setActiveTabKey1] = useState("tab1");
  const onTab1Change = (key) => {
    setActiveTabKey1(key);
  };

  return (
    <Card
      style={{ width: "100%" }}
      title="Model selection"
      tabList={tabList}
      activeTabKey={activeTabKey1}
      onTabChange={onTab1Change}
    >
      {contentList[activeTabKey1]}
    </Card>
  );
}

export default CardModel;
