import React, { Component } from "react";

import "./sidebar.css";

class Sidebar extends Component {
  state = {};
  render() {
    return (
      <div className="sidebar">
        <h1 className="titleText">
            2b2t.Place
        </h1>
        {this.props.children}
      </div>
    );
  }
}

export default Sidebar;
