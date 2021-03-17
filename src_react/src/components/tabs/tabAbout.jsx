import React, { Component } from "react";

import "./tabAbout.css";

class TabAbout extends Component {
  state = {};

  render() {
    return (
      <div className="tabAbout">
        <p>This is a mapart that we build one pixel at a time!</p>
        <p>
          Get started by joining the{" "}
          <a
            href="https://discord.gg/HgWN6tJ8zv"
            target="_blank"
            rel="noopener noreferrer"
          >
            Discord
          </a>
        </p>
        <p>
          Inspired by{" "}
          <a
            href="https://www.reddit.com/r/place/"
            target="_blank"
            rel="noopener noreferrer"
          >
            r/place
          </a>{" "}
          and{" "}
          <a
            href="https://rebane2001.com/mapartcraft/"
            target="_blank"
            rel="noopener noreferrer"
          >
            MapartCraft
          </a>
        </p>
        <nav id="nav">
          <a href="/api">API</a>
          <a
            href="https://github.com/SelfAdjointOperator"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </nav>
      </div>
    );
  }
}

export default TabAbout;
