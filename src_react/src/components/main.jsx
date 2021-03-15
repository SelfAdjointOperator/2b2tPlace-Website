import React, { Component } from "react";

import Sidebar from "./sidebar/sidebar";
import TabAbout from "./tabs/tabAbout";
import TabChoose from "./tabs/tabChoose";
import TabHistory from "./tabs/tabHistory";
import TabLeaderboards from "./tabs/tabLeaderboards";
import MapWindow from "./mapWindow/mapWindow";
import MapToolbar from "./mapWindow/mapToolbar";
import Map from "./mapWindow/map";

import "./main.css";

class Main extends Component {
  state = {
    activeTabId: 0,
  };

  tabs = [
    { id: 0, title: "About", content: <TabAbout /> },
    { id: 1, title: "Choose Pixel", content: <TabChoose /> },
    { id: 2, title: "History", content: <TabHistory /> },
    { id: 3, title: "Leaderboards", content: <TabLeaderboards /> },
  ];

  handleTabChange = (tabId) => {
    this.setState({ activeTabId: tabId });
    console.log(
      this.tabs.filter((tab) => tab.id === this.state.activeTabId)[0]
        .content
    );
  };

  render() {
    return (
      <div className="main">
        <Sidebar>
          {
            this.tabs.filter(
              (tab) => tab.id === this.state.activeTabId
            )[0].content
          }
        </Sidebar>
        <MapWindow>
          <MapToolbar
            activeTabId={this.state.activeTabId}
            tabs={this.tabs}
            onTabChange={(tabId) => this.handleTabChange(tabId)}
          />
          <Map />
        </MapWindow>
      </div>
    );
  }
}

export default Main;
