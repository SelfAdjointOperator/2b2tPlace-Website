import React, { Component } from "react";

import "./tabPixel.css";

import FormSubmit from "./formSubmit";

class TabPixel extends Component {
  render() {
    const {
      activePixel,
      onFormSubmitChange_X,
      onFormSubmitChange_Y,
      allJSONsLoaded,
      coloursJSON,
      colourIdLookupJSON,
      onFormError,
      onBlockChange,
    } = this.props;
    return (
      <div className="tabPixel">
        <h2>Edit a pixel, click the map!</h2>
        <FormSubmit
          activePixel={activePixel}
          onFormSubmitChange_X={onFormSubmitChange_X}
          onFormSubmitChange_Y={onFormSubmitChange_Y}
          allJSONsLoaded={allJSONsLoaded}
          coloursJSON={coloursJSON}
          colourIdLookupJSON={colourIdLookupJSON}
          onFormError={onFormError}
          onBlockChange={onBlockChange}
        ></FormSubmit>
      </div>
    );
  }
}

export default TabPixel;
