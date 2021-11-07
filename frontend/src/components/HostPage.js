import React, { Component } from "react";
import { render } from "react-dom";

import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import { Button, Typography, Textfield, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel, Grid } from "@material-ui/core";

export default class HostPage extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            participants: 0,
            questions: 0,
            host: false,
            session_id: -1,
        };
        this.session_code = this.props.match.params.session_code;

        this.validateHost();
        this.validateHost = this.validateHost.bind(this);
        this.getSessionInfo();
        // this.props.getSessionInfo();
        this.getSessionInfo = this.getSessionInfo.bind(this);
        this.handleEndSession = this.handleEndSession.bind(this);
    }   

    getSessionInfo = () => {
        fetch('/api/get-session?session_code=' + this.session_code).then((response) => 
            response.json()
        ).then((data) => {
            console.log(data);
            this.setState({
                num_participants: data.num_participants,
                num_questions: data.num_questions,
                host: data.is_host,
                session_id: data.id
            }); 
        });
    }

    validateHost() {
        fetch('/api/validate-host?session_code=' + this.session_code).then((response) => {
            console.log(response);
            if (response.status !== 200) {
                this.props.history.push('/');
            }
        })
    }

    handleEndSession () {
        const request = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        }
        fetch('/api/delete', request).then((_response) => {
            this.props.history.push('/');
        });
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="left">
                    <Button color='secondary' onClick={this.handleEndSession}>End Session</Button>
                </Grid>
                <Grid item xs={12} align="left">
                    <p>SESSION {this.session_code}</p>
                </Grid>
                <Grid item xs={12} align="center">
                    <p>PARTICIPANTS {this.state.participants}</p>
                </Grid>
                <Grid item xs={12} align="right">
                    <p>QUESTIONS {this.state.questions}</p>
                </Grid>
            </Grid>
        );
    }
}