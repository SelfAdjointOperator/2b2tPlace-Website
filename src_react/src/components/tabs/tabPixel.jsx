import React, { Component } from "react";

import "./tabPixel.css";

import FormSubmit from "./formSubmit";

class TabPixel extends Component {
  handleFormSubmitChange_X = (x) => {
    this.props.onFormSubmitChange_X(x)
  }

  handleFormSubmitChange_Y = (y) => {
    this.props.onFormSubmitChange_Y(y)
  }

  render() {
    return (
      <div className="tabPixel">
        <h2>Pixel</h2>
        <FormSubmit
          activePixel={this.props.activePixel}
          onFormSubmitChange_X={this.handleFormSubmitChange_X}
          onFormSubmitChange_Y={this.handleFormSubmitChange_Y}
        ></FormSubmit>
      </div>
    );
  }
}

export default TabPixel;
