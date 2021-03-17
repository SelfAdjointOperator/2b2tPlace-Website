import React, { Component } from "react";

import "./map.css";
import E_pixelState from "./E_pixelState";

class Map extends Component {
  mapDrawn = false;

  // PROPS
  // allJSONsLoaded
  // coloursJSON
  // colourIdLookupJSON
  // pixels
  // activePixel
  // activePixelState
  // activePixelPotentialColour
  // onPixelClicked

  drawCanvasPixels = () => {
    const canvas = this.refs.canvas;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    var img = new window.Image();
    img.addEventListener("load", () => {
      canvas.getContext("2d").drawImage(img, 0, 0, 140, 140);
    });
    img.setAttribute("src", "/root/static/images/map_background.png");
    img.onload = () => {
      this.props.pixels.forEach((element) => {
        let colourId = element["colourId"];
        let colourIdInfo = this.props.colourIdLookupJSON[colourId];
        ctx.fillStyle = this.props.coloursJSON[colourIdInfo["colourSetNumber"]][
          "tones"
        ][colourIdInfo["tone"]];
        ctx.fillRect(
          parseInt(element["x"]) + 6,
          parseInt(element["y"]) + 6,
          1,
          1
        );
      });
    };
  };

  getPixelColourFromPixels(x, y) {
    let colour;
    this.props.pixels.forEach((pixel) => {
      if (parseInt(pixel["x"]) === x && parseInt(pixel["y"]) === y) {
        let colourId = pixel["colourId"];
        let colourIdInfo = this.props.colourIdLookupJSON[colourId];
        colour = this.props.coloursJSON[colourIdInfo["colourSetNumber"]][
          "tones"
        ][colourIdInfo["tone"]];
      }
    });
    return colour;
  }

  getRandomColor() {
    let letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  colourFromColourSetNumberAndBlockNumber(colourSetNumber, blockNumber) {
    return this.props.coloursJSON[colourSetNumber.toString()]["tones"][
      "normal"
    ];
  }

  plotPixel(x, y, colour) {
    const canvas = this.refs.canvas;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    ctx.fillStyle = colour;
    ctx.fillRect(parseInt(x) + 6, parseInt(y) + 6, 1, 1);
  }

  rePlotOriginalPixel(x, y) {
    let colour = this.getPixelColourFromPixels(x, y);
    this.plotPixel(x, y, colour);
  }

  flashPixelLoop(x, y) {
    try {
      if (
        this.props.activePixelState !== E_pixelState.FLASHING ||
        this.props.activePixel.x !== x ||
        this.props.activePixel.y !== y
      ) {
        this.rePlotOriginalPixel(x, y);
        return;
      } else {
        this.plotPixel(x, y, this.getRandomColor());
        window.requestAnimationFrame(() => this.flashPixelLoop(x, y));
      }
    } catch (error) {
      console.log(error);
      return;
    }
  }

  handleCanvasClick = (event) => {
    // function to ignore canvas clicks if map not plotted yet
    // and to work out the map X and Y coords clicked
    if (!this.mapDrawn) {
      return;
    }
    const containerRect = this.refs.mapContainer.getBoundingClientRect();
    const mapRect = this.refs.canvas.getBoundingClientRect();
    const pixelSize = mapRect.width / 140;
    const x = Math.floor((event.clientX - mapRect.left) / pixelSize);
    let y;
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
    const actualX = x - 6;
    const actualY = y - 6;
    if (0 <= actualX && actualX < 128 && 0 <= actualY && actualY < 128) {
      this.handleCanvasClickProper(actualX, actualY);
    }
  };

  handleCanvasClickProper = (x, y) => {
    this.props.onPixelClicked(x, y);
  };

  getSnapshotBeforeUpdate(prevProps, prevState) {
    if (prevProps.activePixel.x !== null) {
      this.rePlotOriginalPixel(
        prevProps.activePixel.x,
        prevProps.activePixel.y
      );
    }
    return null;
  }

  componentDidUpdate = () => {
    if (this.mapDrawn) {
      switch (this.props.activePixelState) {
        case E_pixelState.FLASHING:
          window.requestAnimationFrame(() =>
            this.flashPixelLoop(
              this.props.activePixel.x,
              this.props.activePixel.y
            )
          );
          break;
        case E_pixelState.POTENTIALCOLOUR:
          window.requestAnimationFrame(() =>
            this.plotPixel(
              this.props.activePixel.x,
              this.props.activePixel.y,
              this.colourFromColourSetNumberAndBlockNumber(
                this.props.activePixelPotentialColour.colourSetNumber,
                this.props.activePixelPotentialColour.blockNumber
              )
            )
          );
          break;
        default:
          break;
      }
    } else if (this.props.allJSONsLoaded) {
      this.drawCanvasPixels();
      this.mapDrawn = true;
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
          onClick={this.handleCanvasClick}
        />
      </div>
    );
  }
}

export default Map;
