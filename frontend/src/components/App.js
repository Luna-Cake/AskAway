import React, { Component } from "react";
import { render } from "react-dom";
import RouterStart from "./RouterStart"

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (<div>
                    <RouterStart/>
                </div>)
    }
}

const appDiv = document.getElementById('app');
render(<App/>, appDiv);