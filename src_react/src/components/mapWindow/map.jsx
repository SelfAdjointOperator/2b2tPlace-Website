import React, { Component } from "react";

import "./map.css";

class Map extends Component {
  state = {
    coloursJSON: null,
    colourIdLookupJSON: null,
    pixels: null,
  };

  ongoingFetches = [];

  componentDidMount() {
    this.fetchColours();
    this.fetchColourIdLookup();
    this.fetchCurrentPixels();
  }

  fetchColours() {
    this.handleFetchStart("colours");
    fetch("/root/static/json/colours.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ coloursJSON: data });
          this.handleFetchComplete("colours");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  fetchColourIdLookup() {
    this.handleFetchStart("colourIdLookup");
    fetch("/root/static/json/colourIdLookup.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ colourIdLookupJSON: data });
          this.handleFetchComplete("colourIdLookup");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  fetchCurrentPixels() {
    this.handleFetchStart("currentPixels");
    fetch("/api/pixels.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ pixels: data });
          this.handleFetchComplete("currentPixels");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  handleFetchStart = (fetchName) => {
    this.ongoingFetches = this.ongoingFetches.concat([fetchName]);
  };

  handleFetchComplete = (fetchName) => {
    this.ongoingFetches.splice(this.ongoingFetches.indexOf(fetchName), 1);
    if (this.ongoingFetches.length === 0) {
      this.drawCanvasPixels();
    }
  };

  drawCanvasPixels = () => {
    const canvas = this.refs.canvas;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    var img = new window.Image();
    img.addEventListener("load", function () {
      canvas.getContext("2d").drawImage(img, 0, 0, 140, 140);
    });
    img.setAttribute("src", "/root/static/images/map_background.png");
    img.onload = function () {
      this.state.pixels.forEach(function (element) {
        let colourId = element["colourId"];
        let colourIdInfo = this.state.colourIdLookupJSON[colourId];
        ctx.fillStyle = this.state.coloursJSON[colourIdInfo["colourSetNumber"]][
          "tones"
        ][colourIdInfo["tone"]];
        ctx.fillRect(
          parseInt(element["x"]) + 6,
          parseInt(element["y"]) + 6,
          1,
          1
        );
      }, this);
    }.bind(this);
  };

  handleCanvasClick = (event) => {
    const containerRect = this.refs.mapContainer.getBoundingClientRect();
    const mapRect = this.refs.canvas.getBoundingClientRect();
    const pixelSize = mapRect.width / 140;
    const x = Math.floor((event.clientX - mapRect.left) / pixelSize);
    let y = 0;
    if (containerRect.height < containerRect.width) {
      y = Math.floor((event.clientY - mapRect.top) / pixelSize);
    } else if (
      event.clientY - mapRect.top >= (mapRect.height - mapRect.width) / 2 &&
      event.clientY - mapRect.top <= (mapRect.height + mapRect.width) / 2
    ) {
      y = Math.floor(
        (event.clientY - (mapRect.top + (mapRect.height - mapRect.width) / 2)) /
          pixelSize
      );
    } else {
      y = 0;
    }
    if (x >= 6 && x < 134 && y >= 6 && y < 134) {
      const actualX = x - 6;
      const actualY = y - 6;
      alert("x: " + actualX + " y: " + actualY);
    }
  };

  render() {
    return (
      <div className="mapContainer" ref="mapContainer">
        <canvas
          className="mapCanvas"
          width="140"
          height="140"
          ref="canvas"
          onMouseDown={this.handleCanvasClick}
        />
      </div>
    );
  }
}

export default Map;
