import React, { Component } from "react";

import "./mapWindow.css";

class MapWindow extends Component {
  state = {};
  render() {
    return <div className="mapWindow">
      {this.props.children}
    </div>;
  }
}

export default MapWindow;
