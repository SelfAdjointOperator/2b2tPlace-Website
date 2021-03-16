import React, { Component } from "react";

import "./formSubmit.css";

class FormSubmit extends Component {
  state = {};

  onCoordsChange_X = (e) => {
    this.props.onFormSubmitChange_X(parseInt(e.target.value))
  };

  onCoordsChange_Y = (e) => {
    this.props.onFormSubmitChange_Y(parseInt(e.target.value))
  };

  render() {
    let xList = [];
    let yList = [];
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
      if (i === this.props.activePixel.y) {
        yList.push(
          <option key={i} value={i} selected>
            {i}
          </option>
        );
      } else {
        yList.push(
          <option key={i} value={i}>
            {i}
          </option>
        );
      }
    }
    return (
      <form action="#" method="POST" id="formSubmit">
        <input
          id="fsp_auth_token"
          name="fsp_auth_token"
          placeholder="Token"
          required
          type="text"
        />
        <div>
          X:
          <select
            id="fsp_coordinate_x"
            name="fsp_coordinate_x"
            onChange={this.onCoordsChange_X}
            required
          >
            {xList}
          </select>
        </div>
        <div>
          Y:
          <select
            id="fsp_coordinate_y"
            name="fsp_coordinate_y"
            onChange={this.onCoordsChange_Y}
            required
          >
            {yList}
          </select>
        </div>
        <select id="fsp_colourId" name="fsp_colourId" required>
          <option value="TODO">TODO</option>
        </select>
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
        <input type="submit" value="Post"></input>
      </form>
    );
  }
}

export default FormSubmit;
