import React, { Component } from "react";

import "./formSubmit.css";

class FormSubmit extends Component {
  state = {};

  // PROPS
  // activePixel
  // onFormSubmitChange_X
  // onFormSubmitChange_Y
  // allJSONsLoaded
  // coloursJSON
  // colourIdLookupJSON
  // onFormError
  // onBlockChange

  handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    fetch("/api/submit.json", {
      method: "POST",
      body: data,
      credentials: "include",
    })
      .then(
        (response) => {
            return response.json();
        }
      )
      .then((data) => {
        this.props.onFormError(data);
      })
      .catch(function (error) {
        console.log("error", error);
      });
  }

  onCoordsChange_X = (e) => {
    this.props.onFormSubmitChange_X(parseInt(e.target.value));
  };

  onCoordsChange_Y = (e) => {
    this.props.onFormSubmitChange_Y(parseInt(e.target.value));
  };

  onBlockChange = (colourSetNumber, blockNumber) => {
    this.props.onBlockChange(colourSetNumber, blockNumber);
  }

  generateOptions_X() {
    let xList = [];
    for (let i = 0; i < 128; i++) {
      if (i === this.props.activePixel.x) {
        xList.push(
          <option key={i} value={i.toString()} selected>
            {i.toString()}
          </option>
        );
      } else {
        xList.push(
          <option key={i} value={i.toString()}>
            {i.toString()}
          </option>
        );
      }
    }
    return xList;
  }

  generateOptions_Y() {
    let yList = [];
    for (let i = 0; i < 128; i++) {
      if (i === this.props.activePixel.y) {
        yList.push(
          <option key={i} value={i.toString()} selected>
            {i.toString()}
          </option>
        );
      } else {
        yList.push(
          <option key={i} value={i.toString()}>
            {i.toString()}
          </option>
        );
      }
    }
    return yList;
  }

  generateFormColours = () => {
    let { allJSONsLoaded, coloursJSON } = this.props;
    if (allJSONsLoaded === false) {
      return;
    }
    return Object.keys(coloursJSON).map((key) => {
      return (
        <div className="colourSetDiv" key={key}>
          {Object.keys(coloursJSON[key]["blocks"]).map((key2) => {
            return (
              <div key={key2} className="formTextureImageContainer">
                <label className="radioLabel">
                  <input
                    required
                    type="radio"
                    name="fsp_colourId"
                    value={
                      coloursJSON[key]["blocks"][key2]["blockId"]["normal"]
                    }
                  />
                  <img
                    alt={coloursJSON[key]["blocks"][key2]["blockName"]}
                    src="/root/static/images/textures.png"
                    className="formTextureImage"
                    style={{
                      backgroundImage: "/root/static/images/textures.png",
                      margin:
                        "-" +
                        (32 * parseInt(key)).toString() +
                        "px 0px 0px -" +
                        (32 * parseInt(key2)).toString() +
                        "px",
                    }}
                    onClick={() => this.onBlockChange(key, key2)}
                  />
                </label>
              </div>
            );
          })}
        </div>
      );
    });
  }

  render() {
    let xOptions = this.generateOptions_X();
    let yOptions = this.generateOptions_Y();
    let formColours = this.generateFormColours();
    return (
      <form onSubmit={this.handleSubmit} id="formSubmit">
        <div id="formColours">{formColours}</div>
        <div id="restOfForm">
          <div id="xDiv">
            X:
            <select
              id="fsp_coordinate_x"
              name="fsp_coordinate_x"
              onChange={this.onCoordsChange_X}
              required
            >
              {xOptions}
            </select>
          </div>
          <div id="yDiv">
            Y:
            <select
              id="fsp_coordinate_y"
              name="fsp_coordinate_y"
              onChange={this.onCoordsChange_Y}
              required
            >
              {yOptions}
            </select>
          </div>
          <ul id="fsp_anonymise">
            <li>
              <input
                id="fsp_anonymise-0"
                name="fsp_anonymise"
                type="radio"
                value="public"
                defaultChecked
              />
              <label htmlFor="fsp_anonymise-0">
                Show my Discord Tag publicly
              </label>
            </li>
            <li>
              <input
                id="fsp_anonymise-1"
                name="fsp_anonymise"
                type="radio"
                value="anonymous"
              />
              <label htmlFor="fsp_anonymise-1">Keep me anonymous</label>
            </li>
          </ul>
          <input id="submitButton" type="submit" value="Submit!" />
        </div>
      </form>
    );
  }
}

export default FormSubmit;
