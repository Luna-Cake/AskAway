import React, { Component } from "react";
import { render } from "react-dom";
import ParticipantEntry from "./ParticipantEntry";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import HostPage from "./HostPage";
// import { getSessionInfo } from "./HostPage";
import InactiveError from "./InactiveError";
import EntryDesign from './Entry';

import { Button, Typography, Textfield, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel } from "@material-ui/core";
import Participant from "./Participant";

export default class RouterStart extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (<Router>
                    <Switch>
                        <Route exact path='/' component={EntryDesign}></Route>
                        <Route path='/host/:session_code' component={HostPage}></Route>
                        <Route path='/join' component={ParticipantEntry}></Route>
                        <Route path='/session/:session_code' component={Participant}></Route>
                        <Route path='/error' component={InactiveError}></Route>
                    </Switch>
                </Router>);
    }
}