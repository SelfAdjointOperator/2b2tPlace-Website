import React, { Component } from "react";

import Sidebar from "./sidebar/sidebar";
import TabAbout from "./tabs/tabAbout";
import TabPixel from "./tabs/tabPixel";
import TabHistory from "./tabs/tabHistory";
import TabLeaderboards from "./tabs/tabLeaderboards";
import MapWindow from "./mapWindow/mapWindow";
import MapToolbar from "./mapWindow/mapToolbar";
import Map from "./mapWindow/map";

import "./main.css";

class Main extends Component {
  state = {
    activeTabId: 0,
    activePixel: { x: null, y: null },
  };

  handleTabChange = (tabId) => {
    this.setState({
      activeTabId: tabId,
    });
  };

  handleMapPixelClicked = (x, y) => {
    this.setState({ activePixel: { x, y } });
    this.handleTabChange(1);
  };

  handleFormSubmitChange_X = (x) => {
    this.setState({
      activePixel: {
        x: x,
        y: this.state.activePixel.y,
      },
    });
  };

  handleFormSubmitChange_Y = (y) => {
    this.setState({
      activePixel: {
        x: this.state.activePixel.x,
        y: y,
      },
    });
  };

  render() {
    let tabs = [
      { id: 0,
        title: "About",
        content: <TabAbout />
      },
      {
        id: 1,
        title: "Pixel",
        content: (
          <TabPixel
            activePixel={this.state.activePixel}
            onFormSubmitChange_X={this.handleFormSubmitChange_X}
            onFormSubmitChange_Y={this.handleFormSubmitChange_Y}
          />
        ),
      },
      { id: 2,
        title: "History",
        content: <TabHistory />
      },
      {
        id: 3,
        title: "Leaderboards",
        content: <TabLeaderboards />
      },
    ];
    return (
      <div className="main">
        <Sidebar>
          {tabs.filter((tab) => tab.id === this.state.activeTabId)[0].content}
        </Sidebar>
        <MapWindow>
          <MapToolbar
            activeTabId={this.state.activeTabId}
            tabs={tabs}
            onTabChange={this.handleTabChange}
          />
          <Map
            activePixel={this.state.activePixel}
            onPixelClicked={this.handleMapPixelClicked}
          />
        </MapWindow>
      </div>
    );
  }
}

export default Main;
