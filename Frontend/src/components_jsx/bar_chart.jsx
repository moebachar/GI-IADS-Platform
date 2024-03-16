import React, { Component } from "react";
import Chart from "react-apexcharts";

class BarChart extends Component {
  state = {
    series: [
      {
        name: "Width",
        data: this.props.width || [],
      },
      {
        name: "Height",
        data: this.props.height || [],
      },
    ],
    options: {
      chart: {
        type: "bar",
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "55%",
          endingShape: "rounded",
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ["transparent"],
      },
      xaxis: {
        categories: this.props.height
          ? this.generateIndexList(1, this.props.height.length || 0)
          : [],
      },
      yaxis: {
        title: {
          text: "Height & Width (px)",
        },
      },
      fill: {
        opacity: 1,
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + " px";
          },
        },
      },
    },
  };

  componentDidUpdate(prevProps) {
    if (
      prevProps.height !== this.props.height ||
      prevProps.width !== this.props.width
    ) {
      // Update the state or perform any necessary actions when height or width changes
      this.setState((prevState) => ({
        series: [
          { name: "Width", data: this.props.width || [] },
          { name: "Height", data: this.props.height || [] },
        ],
      }));
    }
  }

  generateIndexList(start, length) {
    return Array.from({ length }, (_, index) => start + index);
  }

  render() {
    return (
      <Chart
        options={this.state.options}
        series={this.state.series}
        type="bar"
        height={350}
        width={400}
      />
    );
  }
}

export default BarChart;
