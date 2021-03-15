import React, { Component } from "react";

import "./mapToolbar.css";

class MapToolbar extends Component {
  handleTabTitleClick = (tabId) => {
    this.props.onTabChange(tabId);
  };

  render() {
    return (
      <div className="mapToolbar">
        {this.props.tabs.map((tab) =>
          tab.id === this.props.activeTabId ? (
            <div key={tab.id} className="toolbarTabTitleContainer_active">
              <p className="toolbarTabTitle_active">{tab.title}</p>
            </div>
          ) : (
            <div
              key={tab.id}
              className="toolbarTabTitleContainer"
              onClick={() => this.handleTabTitleClick(tab.id)}
            >
              <div className="toolbarTabTitle">{tab.title}</div>
            </div>
          )
        )}
      </div>
    );
  }
}

export default MapToolbar;
