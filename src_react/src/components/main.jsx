import React, { Component } from "react";

import Sidebar from "./sidebar/sidebar";
import TabAbout from "./tabs/tabAbout";
import TabPixel from "./tabs/tabPixel";
import TabHistory from "./tabs/tabHistory";
import TabLeaderboards from "./tabs/tabLeaderboards";
import MapWindow from "./mapWindow/mapWindow";
import MapToolbar from "./mapWindow/mapToolbar";
import Map from "./mapWindow/map";
import E_pixelState from "./mapWindow/E_pixelState";

import "./main.css";

class Main extends Component {
  state = {
    activeTabId: 0,
    activePixel: { x: null, y: null },
    activePixelState: null,
    activePixelPotentialColour: { colourSetNumber: null, blockNumber: null },
    coloursJSON: null,
    colourIdLookupJSON: null,
    pixels: null,
    allJSONsLoaded: false,
    flashMessages: [],
  };

  ongoingFetches = [];

  componentDidMount() {
    this.fetchColours();
    this.fetchColourIdLookup();
    this.fetchCurrentPixels();
  }

  fetchColours() {
    this.handleFetchStart("colours");
    fetch("/root/static/json/colours.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ coloursJSON: data });
          this.handleFetchComplete("colours");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  fetchColourIdLookup() {
    this.handleFetchStart("colourIdLookup");
    fetch("/root/static/json/colourIdLookup.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ colourIdLookupJSON: data });
          this.handleFetchComplete("colourIdLookup");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  fetchCurrentPixels() {
    this.handleFetchStart("currentPixels");
    fetch("/api/pixels.json")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          return Promise.reject({
            // what is this TODO
            status: response.status,
            statusText: response.statusText,
          });
        }
      })
      .then(
        function (data) {
          this.setState({ pixels: data });
          this.handleFetchComplete("currentPixels");
        }.bind(this)
      )
      .catch(function (error) {
        console.log("error", error);
      });
  }

  handleFetchStart = (fetchName) => {
    this.ongoingFetches = this.ongoingFetches.concat([fetchName]);
  };

  handleFetchComplete = (fetchName) => {
    this.ongoingFetches.splice(this.ongoingFetches.indexOf(fetchName), 1);
    if (this.ongoingFetches.length === 0) {
      this.setState({ allJSONsLoaded: true });
    }
  };

  handleTabClick = (tabId) => {
    this.setState({
      activeTabId: tabId,
    });
  };

  handleMapPixelClicked = (x, y) => {
    this.setState({
      activePixel: { x, y },
      activePixelState: E_pixelState.FLASHING,
    });
    if (![1, 2].includes(this.state.activeTabId)) {
      this.handleTabClick(1);
    }
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

  onFormError = (e) => {
    // includes all messages, todo rename as flash instead of error
    let newFlashMessages = [];
    for (let key in e) {
      newFlashMessages.push(e[key]);
    }
    this.setState({ flashMessages: newFlashMessages });
  };

  onBlockChange = (colourSetNumber, blockNumber) => {
    this.setState({
      activePixelState: E_pixelState.POTENTIALCOLOUR,
      activePixelPotentialColour: { colourSetNumber, blockNumber },
    });
  };

  dismissFlashes = () => {
    this.setState({ flashMessages: [] });
    window.location.reload();
  };

  render() {
    let tabs = [
      { id: 0, title: "About", content: <TabAbout /> },
      {
        id: 1,
        title: "Pixel",
        content: (
          <TabPixel
            activePixel={this.state.activePixel}
            onFormSubmitChange_X={this.handleFormSubmitChange_X}
            onFormSubmitChange_Y={this.handleFormSubmitChange_Y}
            allJSONsLoaded={this.state.allJSONsLoaded}
            coloursJSON={this.state.coloursJSON}
            colourIdLookupJSON={this.state.colourIdLookupJSON}
            onFormError={this.onFormError}
            onBlockChange={this.onBlockChange}
          />
        ),
      },
      { id: 2, title: "History", content: <TabHistory /> },
      {
        id: 3,
        title: "Leaderboards",
        content: <TabLeaderboards />,
      },
    ];
    return (
      <React.Fragment>
        {this.state.flashMessages.length === 0 ? null : (
          <div id="flashDiv">
            <div id="flashDivInner">
              {this.state.flashMessages.map((message) => (
                <p>{message}</p>
              ))}
              <button id="flashDivButton" onClick={this.dismissFlashes}>
                OK
              </button>
            </div>
          </div>
        )}
        <div className="main">
          <Sidebar>
            {tabs.filter((tab) => tab.id === this.state.activeTabId)[0].content}
          </Sidebar>
          <MapWindow>
            <MapToolbar
              activeTabId={this.state.activeTabId}
              tabs={tabs}
              onTabClick={this.handleTabClick}
            />
            <Map
              allJSONsLoaded={this.state.allJSONsLoaded}
              coloursJSON={this.state.coloursJSON}
              colourIdLookupJSON={this.state.colourIdLookupJSON}
              pixels={this.state.pixels}
              activePixel={this.state.activePixel}
              activePixelState={this.state.activePixelState}
              activePixelPotentialColour={this.state.activePixelPotentialColour}
              onPixelClicked={this.handleMapPixelClicked}
            />
          </MapWindow>
        </div>
      </React.Fragment>
    );
  }
}

export default Main;
