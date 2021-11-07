import React, { Component } from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import ParticipantEntry from "./ParticipantEntry";
import { Button, Typography, Textfield, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel, Grid } from "@material-ui/core";

export default class Entry extends Component {
    constructor(props) {
        super(props);
        this.handleSessionCreate = this.handleSessionCreate.bind(this);
        this.handleInSession();
    }

    handleInSession() { 
        fetch('/api/in-session')
        .then((response) => response.json())
        .then((data) => {
            if ('is_host' in data) {
                if (data.is_host)
                    this.props.history.push("/host/" + data.session_code);
                else 
                    this.props.history.push("/session/" + data.session_code);
            }
        });
    }

    handleSessionCreate() {
        const request = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        }
        fetch('/api/create-session', request).then((response) => 
            response.json()
        ).then((data) => this.props.history.push("/host/" + data.session_code));
    }

    render() {
        return (
        <Grid container spacing={1} align="center" alignItems="center" justifyContent="center">
            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    Create or join your live Q/A session!
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText component={'span'}>
                        <div align="center">
                            Host a session by clicking on 'Host Session' or join a session with a code!
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color='primary' variant='contained' disableElevation onClick={this.handleSessionCreate}>Host Session</Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color='secondary' variant='contained' disableElevation to='/join' component={Link}>Join Session</Button>
            </Grid>
        </Grid>
        );
    }
}